# Favorite Links (Django) README

Welcome to our Django project (Favorite Links)! This app offers 2 different user interfaces, the default web UI and a command-line interface. This guide will help you get started with setting up the project on your local machine. The installation and user manual is in the following steps.

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

### 2. Create virtual enviroment and activate

- For Unix/macOS

```bash
py -m venv .venv
source .venv/bin/activate
```

- For Windows

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Install dependencies

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

## Run Application in Web UI

### 1. Start Server

```bash
python manage.py runserver
```

You should now be able to access the development server at http://127.0.0.1:8000/.

### 2. Run Celery for peroidic tasks (Peroidc check for link validity)

- The default peroidic check for link validity is 30 second but you can change it in the scheduleTask function in the view.py file
- A new terminal need to be opened with venv and naviage to the favlinks folder

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

- A new terminal need to be opened with venv and naviage to the favlinks folder
- Wait for celery to start first

```bash
celery -A favlinks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Run Application in Command Line Interface

### 1. Access the CLI

- A new terminal need to be opened with venv and naviage to the favlinks folder

```bash
source .venv/Scripts/activate
cd favlinks
```

### 2. List all the avaliable command

- Use the following command and see the list of command avaliable under the links section

```bash
py manage.py
```

### 3. Use the command

- To see how to use the command use --help after the command

Example:

```bash
py manage.py list_links --help
```

- The command can be used 2 different way with prompt or type it all in one line

Example:

```bash
py manage.py add_link
```

or

```bash
py manage.py add_link --url <your URL> --category <your category> --tags <your tags>
```

### Alternative CLI in Web UI

- An alternative CLI in Web UI is created and can be access through a button on the home page
- This CLI is a working progress and can only perform some simple task

## Additional Notes

- If you encounter any issues during the setup process, please refer to the[ Django documentation](https://docs.djangoproject.com/en/5.0/) or feel free to reach out to the project maintainers for assistance.
