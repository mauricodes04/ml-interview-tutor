## Environment Setup

1. Generate a Django secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. Create a `.env` file with your keys:
```
SECRET_KEY=your_generated_secret_key
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
