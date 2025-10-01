Create a `.env` file:

```
SECRET_KEY=your_django_secret_key_here
OPENAI_API_KEY=sk-...
```

## Setup and Run

```bash
# Create and activate environment
conda env create -f environment.yml
conda activate ml-interview-tutor

# Initialize database and start server
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
