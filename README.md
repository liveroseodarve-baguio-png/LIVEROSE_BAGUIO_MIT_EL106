# LIVEROSE_BAGUIO_MIT_EL106
Performance Integration Task (PIT) Description – EL106

1. Setup Instructions
Step 1: Clone or Create a New Django Project
django-admin startproject myproject
cd myproject
python manage.py startapp users

2. Install Dependencies
Create and activate a virtual environment, then install Django and required libraries:
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
pip install django djangorestframework


Then freeze dependencies: pip freeze > requirements.txt

3. Add the App in settings.py
In myproject/settings.py, include the new app and REST framework:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
]

4. Configure Gmail for Email Verification
Add this to the bottom of your settings.py file:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


Important:
Don’t use your normal Gmail password.
Go to Google Account → Security → App Passwords and generate a new one.
Then paste that app password as EMAIL_HOST_PASSWORD.

5. Configure URLs
In myproject/urls.py:
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]


In users/urls.py:
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_ui, name='register_ui'),
    path('login/', views.login_ui, name='login_ui'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_ui, name='logout_ui'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

6. Create Templates
Inside users/templates/ folder:
base.html → main layout
register.html, login.html, dashboard.html → UI pages
verify_email.html → email body template
activation_invalid.html → error page for bad links
Each child template should start with:
{% extends 'base.html' %}
{% block content %}
<!-- your page content -->
{% endblock %}

7. Views Overview
Main file: users/views.py
Includes:
register_ui → registration form + send verification email
activate → activates account via email link
login_ui → user login
dashboard → only accessible when logged in
logout_ui → logs out user

8. Run Migrations
python manage.py makemigrations
python manage.py migrate

Then create a superuser:
python manage.py createsuperuser

9. Run the Server
python manage.py runserver
Open the site in your browser:
👉 http://127.0.0.1:8000/register/

10. Test the Flow
Register a new account on /register/
Check your Gmail inbox for a verification link
Click the link — your account will be activated
Log in at /login/
You’ll be redirected to /dashboard/
