# Utility_MicroS
Micro Server for Utility functions - Global

Steps to create virtual environment (Windows):
```
python -m pip install virtualenv
python -m virtualenv env_name
 ```

Steps to create django application (Windows):
```
venv\Scripts\activate
python -m pip install django
django-admin startproject project_name
python manage.py startapp app_name
python manage.py createsuperuser
 ```

Steps to migrate changes (Windows):
```
python manage.py makemigrations security utilities app_user database --name migration_name
python manage.py migrate
```

Steps to start server (Windows):
```
python -m pip freeze > requirements.txt
python manage.py runserver
```