from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'profile_user'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),

]
