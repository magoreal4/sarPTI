from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'main'  # Define el espacio de nombres aquí

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
