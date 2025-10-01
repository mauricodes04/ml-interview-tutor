import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from .models import Chat

# Initialize OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=openai_api_key)

# Initialize LangChain
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = Chroma(persist_directory='', embedding_function=embeddings)

def ask_openai(message):
    """Get AI response using context from vector store."""
    docs = vectorstore.similarity_search(message)
    messages = [
        {"role": "system", "content": f"Answer a question given this information: {docs}"},
        {"role": "user", "content": message}
    ]
    
    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=messages
    )
    return response.choices[0].message.content

# Create your views here.
@login_required(login_url='login')
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats':chats})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            auth.login(request, user)
            return redirect('chatbot')
        return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})
        
        try:
            user = User.objects.create_user(username, email, password1)
            auth.login(request, user)
            return redirect('chatbot')
        except Exception:
            return render(request, 'register.html', {'error_message': 'Error creating account'})
    
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')