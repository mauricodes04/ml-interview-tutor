## Setup and Run

# Create and activate environment
cd D:/this/location
conda env create -f environment.yml
conda activate ml-interview-tutor

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Create a `.env` file with your keys:
```
SECRET_KEY=your_generated_secret_key
OPENAI_API_KEY=sk-
```

# Initialize database and start server
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
