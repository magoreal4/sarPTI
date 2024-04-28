from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    
    # # Asegúrate de incluir también las URLs para el proceso completo de restablecimiento
    # path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
