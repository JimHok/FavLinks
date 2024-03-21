# Favorite Links (Django) README

Welcome to our Django project (Favorite Links)! This guide will help you get started with setting up the project on your local machine.

## Prerequisites

- Python 3.x installed on your system
- pip package manager installed
- git installed (if cloning the project repository)
- redis installed

## Installation

### 1. Clone the repository (if you haven't already)

```bash
git clone https://github.com/JimHok/FavLinks.git
```

### 2. For Unix/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. For Windows

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### Important

**_Celery and Celery Beat are needed to run peroidic task, to install please refer to the[ Celery documentation](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django) and the[ Celery beat documentation](https://django-celery-beat.readthedocs.io/en/latest/)_**

## Database Setup

### 1. Navigage to folder

```bash
cd favlinks
```

### 2. Make migrations

```bash
python manage.py makemigrations
```

### 3. Apply migrations

```bash
python manage.py migrate
```

## Run Application

### 1. Start Server

```bash
python manage.py runserver
```

You should now be able to access the development server at http://127.0.0.1:8000/.

### 2. Run Celery for peroidic tasks

- A new terminal need to be opened with venv

```bash
source .venv/Scripts/activate
cd favlinks
```

- For Unix/macOS

```bash
celery -A favlinks worker -l info
```

- For Windows

```bash
celery -A favlinks worker -l info -P gevent
```

### 3. Run Celery beat for peroidic tasks

- A new terminal need to be opened with venv
- Wait for celery to start first

```bash
source .venv/Scripts/activate
cd favlinks
```

```bash
celery -A favlinks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Additional Notes

- If you encounter any issues during the setup process, please refer to the[ Django documentation](https://docs.djangoproject.com/en/5.0/) or feel free to reach out to the project maintainers for assistance.
