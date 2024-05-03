from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'main'  # Define el espacio de nombres aquí

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    # path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
