
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('update_email/', views.update_email, name='update_email'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_currency/', views.update_currency, name='update_currency'),
]