"""
================================================================
   DJANGO TASK MANAGER — Auto Setup Script
   Level 3 Task 1: Django Web App with Authentication
================================================================

   HOW TO USE:
   1. Install Django:  pip install django
   2. Run this file:   python setup_project.py
   3. Follow the instructions printed at the end!

================================================================
"""

import os
import sys

BASE = "taskmanager_project"

def create(path, content=""):
    """Create a file with given content"""
    full_path = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ Created: {path}")

def mkdir(path):
    os.makedirs(os.path.join(BASE, path), exist_ok=True)

print("""
╔══════════════════════════════════════════════════╗
║     DJANGO TASK MANAGER — Project Setup         ║
║     Building your project files...              ║
╚══════════════════════════════════════════════════╝
""")

# ── Create folder structure ──
for folder in [
    "taskmanager", "accounts", "tasks",
    "templates/accounts", "templates/tasks",
    "templates/admin", "static/css"
]:
    mkdir(folder)

# ════════════════════════════════════════
#   requirements.txt
# ════════════════════════════════════════
create("requirements.txt", """django>=4.2
pillow>=10.0
""")

# ════════════════════════════════════════
#   manage.py
# ════════════════════════════════════════
create("manage.py", """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""")

# ════════════════════════════════════════
#   taskmanager/settings.py
# ════════════════════════════════════════
create("taskmanager/settings.py", """
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-change-this-in-production-xyz123'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'taskmanager.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'taskmanager.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/tasks/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Email settings (for password reset)
# For development — prints email to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
""")

# ════════════════════════════════════════
#   taskmanager/urls.py
# ════════════════════════════════════════
create("taskmanager/urls.py", """
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/',    admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tasks/',    include('tasks.urls')),
    path('',          RedirectView.as_view(url='/accounts/login/')),
]
""")

# ════════════════════════════════════════
#   taskmanager/__init__.py
# ════════════════════════════════════════
create("taskmanager/__init__.py", "")
create("taskmanager/wsgi.py", """
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
application = get_wsgi_application()
""")

# ════════════════════════════════════════
#   accounts/models.py
# ════════════════════════════════════════
create("accounts/__init__.py", "")
create("accounts/models.py", """
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user',  'Regular User'),
    ]
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    bio        = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_admin_role(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.user.username} ({self.role})"
""")

# ════════════════════════════════════════
#   accounts/forms.py
# ════════════════════════════════════════
create("accounts/forms.py", """
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)
    role       = forms.ChoiceField(choices=[('user','Regular User'),('admin','Admin')])

    class Meta:
        model  = User
        fields = ['username','first_name','last_name','email','password1','password2','role']

    def save(self, commit=True):
        user            = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        if commit:
            user.save()
            role = self.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)
            if role == 'admin':
                user.is_staff = True
                user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
""")

# ════════════════════════════════════════
#   accounts/views.py
# ════════════════════════════════════════
create("accounts/views.py", """
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Account created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            messages.success(request,
                'Password reset email sent! Check your console (development mode).')
            form.save(request=request,
                      use_https=False,
                      email_template_name='accounts/password_reset_email.html')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/password_reset.html', {'form': form})
""")

# ════════════════════════════════════════
#   accounts/urls.py
# ════════════════════════════════════════
create("accounts/urls.py", """
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/',       views.register_view,    name='register'),
    path('login/',          views.login_view,        name='login'),
    path('logout/',         views.logout_view,       name='logout'),
    path('profile/',        views.profile_view,      name='profile'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
""")

create("accounts/admin.py", """
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'role', 'created_at']
    list_filter   = ['role']
    search_fields = ['user__username', 'user__email']
""")

# ════════════════════════════════════════
#   tasks/models.py
# ════════════════════════════════════════
create("tasks/__init__.py", "")
create("tasks/models.py", """
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
    ]
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
    ]

    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority    = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status      = models.CharField(max_length=15, choices=STATUS_CHOICES,   default='pending')
    due_date    = models.DateField(null=True, blank=True)
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def is_overdue(self):
        from datetime import date
        return self.due_date and self.due_date < date.today() and self.status != 'completed'

    def __str__(self):
        return self.title
""")

# ════════════════════════════════════════
#   tasks/forms.py
# ════════════════════════════════════════
create("tasks/forms.py", """
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = ['title','description','priority','status','due_date']
        widgets = {
            'title':       forms.TextInput(attrs={'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description'}),
            'due_date':    forms.DateInput(attrs={'type': 'date'}),
        }
""")

# ════════════════════════════════════════
#   tasks/views.py
# ════════════════════════════════════════
create("tasks/views.py", """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from .models import Task
from .forms import TaskForm

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'profile') or not request.user.profile.is_admin_role():
            messages.error(request, 'You need admin access for this!')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper)

@login_required
def dashboard(request):
    user  = request.user
    tasks = Task.objects.filter(created_by=user)
    stats = {
        'total':       tasks.count(),
        'pending':     tasks.filter(status='pending').count(),
        'in_progress': tasks.filter(status='in_progress').count(),
        'completed':   tasks.filter(status='completed').count(),
        'overdue':     sum(1 for t in tasks if t.is_overdue()),
    }
    recent_tasks = tasks[:5]
    return render(request, 'tasks/dashboard.html', {
        'stats': stats, 'recent_tasks': recent_tasks
    })

@login_required
def task_list(request):
    tasks    = Task.objects.filter(created_by=request.user)
    search   = request.GET.get('search', '')
    priority = request.GET.get('priority', '')
    status   = request.GET.get('status', '')

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    if priority:
        tasks = tasks.filter(priority=priority)
    if status:
        tasks = tasks.filter(status=status)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks, 'search': search,
        'priority': priority, 'status': status
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task            = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit', 'task': task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_complete(request, pk):
    task        = get_object_or_404(Task, pk=pk, created_by=request.user)
    task.status = 'completed'
    task.save()
    messages.success(request, f'Task "{task.title}" marked as completed!')
    return redirect('task_list')

@admin_required
def admin_panel(request):
    all_users = User.objects.all()
    all_tasks = Task.objects.all()
    stats = {
        'total_users': all_users.count(),
        'total_tasks': all_tasks.count(),
        'completed':   all_tasks.filter(status='completed').count(),
        'pending':     all_tasks.filter(status='pending').count(),
    }
    return render(request, 'tasks/admin_panel.html', {
        'stats': stats, 'users': all_users, 'tasks': all_tasks[:20]
    })
""")

# ════════════════════════════════════════
#   tasks/urls.py
# ════════════════════════════════════════
create("tasks/urls.py", """
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',        views.dashboard,    name='dashboard'),
    path('',                  views.task_list,    name='task_list'),
    path('create/',           views.task_create,  name='task_create'),
    path('edit/<int:pk>/',    views.task_edit,    name='task_edit'),
    path('delete/<int:pk>/',  views.task_delete,  name='task_delete'),
    path('complete/<int:pk>/',views.task_complete,name='task_complete'),
    path('admin-panel/',      views.admin_panel,  name='admin_panel'),
]
""")

create("tasks/admin.py", """
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ['title','created_by','priority','status','due_date','created_at']
    list_filter   = ['priority','status']
    search_fields = ['title','description']
""")

# ════════════════════════════════════════
#   BASE TEMPLATE
# ════════════════════════════════════════
create("templates/base.html", """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}Task Manager{% endblock %}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; }

    /* NAVBAR */
    .navbar {
      background: linear-gradient(135deg, #1B3A5C, #2E75B6);
      padding: 0 30px; display: flex;
      align-items: center; justify-content: space-between;
      height: 60px; box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .navbar .brand { color: white; font-size: 22px; font-weight: bold; text-decoration: none; }
    .navbar .nav-links a {
      color: rgba(255,255,255,0.85); text-decoration: none;
      margin-left: 20px; font-size: 14px; padding: 6px 12px;
      border-radius: 6px; transition: background 0.2s;
    }
    .navbar .nav-links a:hover { background: rgba(255,255,255,0.15); color: white; }
    .navbar .nav-links .btn-logout {
      background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
    }

    /* MAIN */
    .container { max-width: 1100px; margin: 30px auto; padding: 0 20px; }

    /* MESSAGES */
    .messages { margin-bottom: 20px; }
    .alert {
      padding: 12px 18px; border-radius: 8px; margin-bottom: 10px;
      font-size: 14px; font-weight: 500;
    }
    .alert-success { background: #d4edda; color: #155724; border-left: 4px solid #28a745; }
    .alert-error   { background: #f8d7da; color: #721c24; border-left: 4px solid #dc3545; }
    .alert-info    { background: #d1ecf1; color: #0c5460; border-left: 4px solid #17a2b8; }

    /* CARDS */
    .card {
      background: white; border-radius: 12px; padding: 25px;
      box-shadow: 0 2px 15px rgba(0,0,0,0.08); margin-bottom: 20px;
    }
    .card-title { font-size: 20px; font-weight: bold; color: #1B3A5C; margin-bottom: 15px; }

    /* STATS */
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px,1fr)); gap: 15px; margin-bottom: 25px; }
    .stat-card {
      background: white; border-radius: 12px; padding: 20px; text-align: center;
      box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-top: 4px solid #2E75B6;
    }
    .stat-card.green  { border-top-color: #28a745; }
    .stat-card.orange { border-top-color: #fd7e14; }
    .stat-card.red    { border-top-color: #dc3545; }
    .stat-card.teal   { border-top-color: #20c997; }
    .stat-number { font-size: 36px; font-weight: bold; color: #1B3A5C; }
    .stat-label  { font-size: 13px; color: #888; margin-top: 5px; }

    /* BUTTONS */
    .btn {
      display: inline-block; padding: 9px 18px; border-radius: 8px;
      text-decoration: none; font-size: 14px; font-weight: 500;
      cursor: pointer; border: none; transition: all 0.2s;
    }
    .btn-primary  { background: #2E75B6; color: white; }
    .btn-primary:hover  { background: #1B3A5C; }
    .btn-success  { background: #28a745; color: white; }
    .btn-success:hover  { background: #218838; }
    .btn-danger   { background: #dc3545; color: white; }
    .btn-danger:hover   { background: #c82333; }
    .btn-warning  { background: #fd7e14; color: white; }
    .btn-secondary{ background: #6c757d; color: white; }
    .btn-sm { padding: 5px 12px; font-size: 12px; }

    /* TABLE */
    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th { background: #1B3A5C; color: white; padding: 12px 15px; text-align: left; }
    td { padding: 11px 15px; border-bottom: 1px solid #eee; }
    tr:hover { background: #f8f9fa; }

    /* BADGES */
    .badge {
      display: inline-block; padding: 3px 10px; border-radius: 20px;
      font-size: 12px; font-weight: 600;
    }
    .badge-high    { background: #ffe0e0; color: #c82333; }
    .badge-medium  { background: #fff3cd; color: #856404; }
    .badge-low     { background: #d4edda; color: #155724; }
    .badge-pending    { background: #e2e3e5; color: #383d41; }
    .badge-progress   { background: #cce5ff; color: #004085; }
    .badge-completed  { background: #d4edda; color: #155724; }
    .badge-overdue    { background: #f8d7da; color: #721c24; }

    /* FORMS */
    .form-group { margin-bottom: 18px; }
    .form-group label { display: block; font-weight: 600; margin-bottom: 6px; color: #444; font-size: 14px; }
    .form-group input,
    .form-group select,
    .form-group textarea {
      width: 100%; padding: 10px 14px; border: 1.5px solid #dee2e6;
      border-radius: 8px; font-size: 14px; transition: border 0.2s;
    }
    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
      outline: none; border-color: #2E75B6; box-shadow: 0 0 0 3px rgba(46,117,182,0.15);
    }
    .errorlist { color: #dc3545; font-size: 12px; margin-top: 4px; list-style: none; }

    /* AUTH PAGES */
    .auth-container {
      min-height: 100vh; display: flex; align-items: center;
      justify-content: center; background: linear-gradient(135deg, #1B3A5C, #2E75B6);
    }
    .auth-card {
      background: white; border-radius: 16px; padding: 40px;
      width: 100%; max-width: 420px; box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    .auth-title { text-align: center; font-size: 26px; font-weight: bold; color: #1B3A5C; margin-bottom: 8px; }
    .auth-subtitle { text-align: center; color: #888; font-size: 14px; margin-bottom: 28px; }
    .auth-link { text-align: center; margin-top: 18px; font-size: 14px; color: #666; }
    .auth-link a { color: #2E75B6; text-decoration: none; font-weight: 600; }

    /* SEARCH BAR */
    .search-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
    .search-bar input, .search-bar select {
      padding: 9px 14px; border: 1.5px solid #dee2e6;
      border-radius: 8px; font-size: 14px;
    }

    /* EMPTY STATE */
    .empty-state { text-align: center; padding: 60px 20px; color: #888; }
    .empty-state h3 { font-size: 22px; margin-bottom: 10px; }

    /* PAGE HEADER */
    .page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 25px; }
    .page-header h1 { font-size: 26px; color: #1B3A5C; }
  </style>
</head>
<body>

{% if user.is_authenticated %}
<nav class="navbar">
  <a href="{% url 'dashboard' %}" class="brand">📋 Task Manager</a>
  <div class="nav-links">
    <a href="{% url 'dashboard' %}">🏠 Dashboard</a>
    <a href="{% url 'task_list' %}">📝 My Tasks</a>
    <a href="{% url 'task_create' %}">➕ New Task</a>
    {% if user.profile.is_admin_role %}
    <a href="{% url 'admin_panel' %}">⚙️ Admin Panel</a>
    {% endif %}
    <a href="{% url 'profile' %}">👤 {{ user.username }}</a>
    <a href="{% url 'logout' %}" class="btn-logout">🚪 Logout</a>
  </div>
</nav>
{% endif %}

<div class="{% if not user.is_authenticated %}auth-container{% else %}container{% endif %}">
  {% if messages %}
  <div class="messages">
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }}">{{ message }}</div>
    {% endfor %}
  </div>
  {% endif %}

  {% block content %}{% endblock %}
</div>

</body>
</html>
""")

# ════════════════════════════════════════
#   LOGIN TEMPLATE
# ════════════════════════════════════════
create("templates/accounts/login.html", """{% extends 'base.html' %}
{% block title %}Login — Task Manager{% endblock %}
{% block content %}
<div class="auth-card">
  <div class="auth-title">🔐 Welcome Back!</div>
  <div class="auth-subtitle">Sign in to your account</div>

  {% if messages %}
  {% for message in messages %}
  <div class="alert alert-{{ message.tags }}">{{ message }}</div>
  {% endfor %}
  {% endif %}

  <form method="post">
    {% csrf_token %}
    <div class="form-group">
      <label>Username</label>
      {{ form.username }}
      {% if form.username.errors %}<ul class="errorlist">{% for e in form.username.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
    </div>
    <div class="form-group">
      <label>Password</label>
      {{ form.password }}
      {% if form.password.errors %}<ul class="errorlist">{% for e in form.password.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
    </div>
    <button type="submit" class="btn btn-primary" style="width:100%;padding:12px;">Login</button>
  </form>

  <div class="auth-link"><a href="{% url 'password_reset' %}">Forgot password?</a></div>
  <div class="auth-link">Don't have an account? <a href="{% url 'register' %}">Register here</a></div>
</div>
{% endblock %}
""")

# ════════════════════════════════════════
#   REGISTER TEMPLATE
# ════════════════════════════════════════
create("templates/accounts/register.html", """{% extends 'base.html' %}
{% block title %}Register — Task Manager{% endblock %}
{% block content %}
<div class="auth-card" style="max-width:480px;">
  <div class="auth-title">📝 Create Account</div>
  <div class="auth-subtitle">Join Task Manager today</div>

  <form method="post">
    {% csrf_token %}
    {% for field in form %}
    <div class="form-group">
      <label>{{ field.label }}</label>
      {{ field }}
      {% if field.errors %}<ul class="errorlist">{% for e in field.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
    </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary" style="width:100%;padding:12px;">Create Account</button>
  </form>

  <div class="auth-link">Already have an account? <a href="{% url 'login' %}">Login here</a></div>
</div>
{% endblock %}
""")

# ════════════════════════════════════════
#   PASSWORD RESET TEMPLATE
# ════════════════════════════════════════
create("templates/accounts/password_reset.html", """{% extends 'base.html' %}
{% block title %}Password Reset{% endblock %}
{% block content %}
<div class="auth-card">
  <div class="auth-title">🔑 Reset Password</div>
  <div class="auth-subtitle">Enter your email to reset your password</div>
  <form method="post">
    {% csrf_token %}
    <div class="form-group">
      <label>Email Address</label>
      {{ form.email }}
    </div>
    <button type="submit" class="btn btn-primary" style="width:100%;padding:12px;">Send Reset Email</button>
  </form>
  <div class="auth-link"><a href="{% url 'login' %}">Back to Login</a></div>
</div>
{% endblock %}
""")

create("templates/accounts/password_reset_confirm.html", """{% extends 'base.html' %}
{% block content %}
<div class="auth-card">
  <div class="auth-title">Set New Password</div>
  <form method="post">{% csrf_token %}{{ form.as_p }}<button type="submit" class="btn btn-primary" style="width:100%">Set Password</button></form>
</div>
{% endblock %}
""")

create("templates/accounts/password_reset_complete.html", """{% extends 'base.html' %}
{% block content %}
<div class="auth-card">
  <div class="auth-title">✅ Password Reset!</div>
  <div class="auth-subtitle">Your password has been reset successfully.</div>
  <a href="{% url 'login' %}" class="btn btn-primary" style="width:100%;display:block;text-align:center;margin-top:15px;">Login Now</a>
</div>
{% endblock %}
""")

create("templates/accounts/password_reset_email.html", """Hello {{ user.username }},
Reset your password: {{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
""")

# ════════════════════════════════════════
#   PROFILE TEMPLATE
# ════════════════════════════════════════
create("templates/accounts/profile.html", """{% extends 'base.html' %}
{% block title %}Profile{% endblock %}
{% block content %}
<div class="page-header">
  <h1>👤 My Profile</h1>
</div>
<div class="card">
  <p><strong>Username:</strong> {{ user.username }}</p>
  <p><strong>Name:</strong> {{ user.first_name }} {{ user.last_name }}</p>
  <p><strong>Email:</strong> {{ user.email }}</p>
  <p><strong>Role:</strong>
    {% if user.profile.role == 'admin' %}
      <span class="badge badge-high">Admin</span>
    {% else %}
      <span class="badge badge-completed">Regular User</span>
    {% endif %}
  </p>
  <p><strong>Member Since:</strong> {{ user.date_joined|date:"d M Y" }}</p>
</div>
{% endblock %}
""")

# ════════════════════════════════════════
#   DASHBOARD TEMPLATE
# ════════════════════════════════════════
create("templates/tasks/dashboard.html", """{% extends 'base.html' %}
{% block title %}Dashboard{% endblock %}
{% block content %}

<div class="page-header">
  <h1>🏠 Dashboard</h1>
  <a href="{% url 'task_create' %}" class="btn btn-primary">➕ New Task</a>
</div>

<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-number">{{ stats.total }}</div>
    <div class="stat-label">Total Tasks</div>
  </div>
  <div class="stat-card orange">
    <div class="stat-number">{{ stats.pending }}</div>
    <div class="stat-label">Pending</div>
  </div>
  <div class="stat-card teal">
    <div class="stat-number">{{ stats.in_progress }}</div>
    <div class="stat-label">In Progress</div>
  </div>
  <div class="stat-card green">
    <div class="stat-number">{{ stats.completed }}</div>
    <div class="stat-label">Completed</div>
  </div>
  <div class="stat-card red">
    <div class="stat-number">{{ stats.overdue }}</div>
    <div class="stat-label">Overdue</div>
  </div>
</div>

<div class="card">
  <div class="card-title">📋 Recent Tasks</div>
  {% if recent_tasks %}
  <table>
    <thead><tr><th>Title</th><th>Priority</th><th>Status</th><th>Due Date</th><th>Actions</th></tr></thead>
    <tbody>
    {% for task in recent_tasks %}
    <tr>
      <td>{{ task.title }}</td>
      <td><span class="badge badge-{{ task.priority }}">{{ task.get_priority_display }}</span></td>
      <td>
        {% if task.is_overdue %}
          <span class="badge badge-overdue">Overdue</span>
        {% else %}
          <span class="badge badge-{{ task.status|slugify }}">{{ task.get_status_display }}</span>
        {% endif %}
      </td>
      <td>{{ task.due_date|default:"—" }}</td>
      <td>
        <a href="{% url 'task_edit' task.pk %}" class="btn btn-warning btn-sm">Edit</a>
        <a href="{% url 'task_complete' task.pk %}" class="btn btn-success btn-sm">Done</a>
      </td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
  <br>
  <a href="{% url 'task_list' %}" class="btn btn-primary">View All Tasks</a>
  {% else %}
  <div class="empty-state">
    <h3>No tasks yet!</h3>
    <p>Create your first task to get started.</p>
    <br>
    <a href="{% url 'task_create' %}" class="btn btn-primary">➕ Create Task</a>
  </div>
  {% endif %}
</div>
{% endblock %}
""")

# ════════════════════════════════════════
#   TASK LIST TEMPLATE
# ════════════════════════════════════════
create("templates/tasks/task_list.html", """{% extends 'base.html' %}
{% block title %}My Tasks{% endblock %}
{% block content %}

<div class="page-header">
  <h1>📝 My Tasks</h1>
  <a href="{% url 'task_create' %}" class="btn btn-primary">➕ New Task</a>
</div>

<div class="card">
  <form method="get" class="search-bar">
    <input type="text" name="search" value="{{ search }}" placeholder="Search tasks...">
    <select name="priority">
      <option value="">All Priorities</option>
      <option value="high"   {% if priority == 'high'   %}selected{% endif %}>High</option>
      <option value="medium" {% if priority == 'medium' %}selected{% endif %}>Medium</option>
      <option value="low"    {% if priority == 'low'    %}selected{% endif %}>Low</option>
    </select>
    <select name="status">
      <option value="">All Status</option>
      <option value="pending"     {% if status == 'pending'     %}selected{% endif %}>Pending</option>
      <option value="in_progress" {% if status == 'in_progress' %}selected{% endif %}>In Progress</option>
      <option value="completed"   {% if status == 'completed'   %}selected{% endif %}>Completed</option>
    </select>
    <button type="submit" class="btn btn-primary">Filter</button>
    <a href="{% url 'task_list' %}" class="btn btn-secondary">Clear</a>
  </form>

  {% if tasks %}
  <table>
    <thead>
      <tr><th>Title</th><th>Priority</th><th>Status</th><th>Due Date</th><th>Actions</th></tr>
    </thead>
    <tbody>
    {% for task in tasks %}
    <tr>
      <td><strong>{{ task.title }}</strong><br><small style="color:#888">{{ task.description|truncatechars:60 }}</small></td>
      <td><span class="badge badge-{{ task.priority }}">{{ task.get_priority_display }}</span></td>
      <td>
        {% if task.is_overdue %}
          <span class="badge badge-overdue">⚠️ Overdue</span>
        {% elif task.status == 'completed' %}
          <span class="badge badge-completed">✅ Completed</span>
        {% elif task.status == 'in_progress' %}
          <span class="badge badge-progress">🔄 In Progress</span>
        {% else %}
          <span class="badge badge-pending">⏳ Pending</span>
        {% endif %}
      </td>
      <td>{{ task.due_date|default:"—" }}</td>
      <td>
        <a href="{% url 'task_edit' task.pk %}"    class="btn btn-warning btn-sm">✏️ Edit</a>
        {% if task.status != 'completed' %}
        <a href="{% url 'task_complete' task.pk %}" class="btn btn-success btn-sm">✅ Done</a>
        {% endif %}
        <a href="{% url 'task_delete' task.pk %}"  class="btn btn-danger btn-sm">🗑️ Delete</a>
      </td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
  {% else %}
  <div class="empty-state">
    <h3>No tasks found!</h3>
    <p>Try different filters or create a new task.</p>
    <br>
    <a href="{% url 'task_create' %}" class="btn btn-primary">➕ Create Task</a>
  </div>
  {% endif %}
</div>
{% endblock %}
""")

# ════════════════════════════════════════
#   TASK FORM TEMPLATE
# ════════════════════════════════════════
create("templates/tasks/task_form.html", """{% extends 'base.html' %}
{% block title %}{{ action }} Task{% endblock %}
{% block content %}
<div class="page-header">
  <h1>{% if action == 'Create' %}➕{% else %}✏️{% endif %} {{ action }} Task</h1>
  <a href="{% url 'task_list' %}" class="btn btn-secondary">← Back</a>
</div>
<div class="card" style="max-width:600px;">
  <form method="post">
    {% csrf_token %}
    {% for field in form %}
    <div class="form-group">
      <label>{{ field.label }}</label>
      {{ field }}
      {% if field.errors %}<ul class="errorlist">{% for e in field.errors %}<li>{{ e }}</li>{% endfor %}</ul>{% endif %}
    </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary">{{ action }} Task</button>
    <a href="{% url 'task_list' %}" class="btn btn-secondary">Cancel</a>
  </form>
</div>
{% endblock %}
""")

# ════════════════════════════════════════
#   DELETE CONFIRM TEMPLATE
# ════════════════════════════════════════
create("templates/tasks/task_confirm_delete.html", """{% extends 'base.html' %}
{% block title %}Delete Task{% endblock %}
{% block content %}
<div class="card" style="max-width:500px;margin:auto;text-align:center;">
  <h2 style="color:#dc3545;">🗑️ Delete Task?</h2>
  <p style="margin:15px 0;">Are you sure you want to delete:</p>
  <p><strong>"{{ task.title }}"</strong></p>
  <p style="color:#888;font-size:14px;">This action cannot be undone!</p>
  <br>
  <form method="post" style="display:inline;">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Yes, Delete</button>
  </form>
  <a href="{% url 'task_list' %}" class="btn btn-secondary" style="margin-left:10px;">Cancel</a>
</div>
{% endblock %}
""")

# ════════════════════════════════════════
#   ADMIN PANEL TEMPLATE
# ════════════════════════════════════════
create("templates/tasks/admin_panel.html", """{% extends 'base.html' %}
{% block title %}Admin Panel{% endblock %}
{% block content %}
<div class="page-header"><h1>⚙️ Admin Panel</h1></div>

<div class="stats-grid">
  <div class="stat-card"><div class="stat-number">{{ stats.total_users }}</div><div class="stat-label">Total Users</div></div>
  <div class="stat-card teal"><div class="stat-number">{{ stats.total_tasks }}</div><div class="stat-label">Total Tasks</div></div>
  <div class="stat-card green"><div class="stat-number">{{ stats.completed }}</div><div class="stat-label">Completed</div></div>
  <div class="stat-card orange"><div class="stat-number">{{ stats.pending }}</div><div class="stat-label">Pending</div></div>
</div>

<div class="card">
  <div class="card-title">👥 All Users</div>
  <table>
    <thead><tr><th>Username</th><th>Email</th><th>Role</th><th>Joined</th></tr></thead>
    <tbody>
    {% for user in users %}
    <tr>
      <td>{{ user.username }}</td>
      <td>{{ user.email }}</td>
      <td>
        {% if user.profile.role == 'admin' %}
          <span class="badge badge-high">Admin</span>
        {% else %}
          <span class="badge badge-completed">User</span>
        {% endif %}
      </td>
      <td>{{ user.date_joined|date:"d M Y" }}</td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</div>

<div class="card">
  <div class="card-title">📋 Recent Tasks (All Users)</div>
  <table>
    <thead><tr><th>Title</th><th>Created By</th><th>Priority</th><th>Status</th></tr></thead>
    <tbody>
    {% for task in tasks %}
    <tr>
      <td>{{ task.title }}</td>
      <td>{{ task.created_by.username }}</td>
      <td><span class="badge badge-{{ task.priority }}">{{ task.get_priority_display }}</span></td>
      <td><span class="badge">{{ task.get_status_display }}</span></td>
    </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
""")

print("""
╔══════════════════════════════════════════════════════╗
║          PROJECT CREATED SUCCESSFULLY!              ║
╚══════════════════════════════════════════════════════╝

NOW FOLLOW THESE STEPS TO RUN YOUR APP:

Step 1 — Install Django:
   pip install django

Step 2 — Go into project folder:
   cd taskmanager_project

Step 3 — Run database migrations:
   python manage.py makemigrations
   python manage.py migrate

Step 4 — Create superuser (admin account):
   python manage.py createsuperuser

Step 5 — Start the server:
   python manage.py runserver

Step 6 — Open your browser and go to:
   http://127.0.0.1:8000

DONE! Your Django Task Manager is LIVE! 🎉

FEATURES:
  ✅ User Registration & Login
  ✅ Logout
  ✅ Password Reset (via email)
  ✅ Admin Role & Regular User Role
  ✅ Admin Panel (admin users only)
  ✅ Create / Edit / Delete Tasks
  ✅ Mark Tasks as Complete
  ✅ Search & Filter Tasks
  ✅ Dashboard with Stats
  ✅ Beautiful UI Design
""")
