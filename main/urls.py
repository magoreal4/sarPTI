from django.urls import path, include
from . import views


app_name = 'main'  # Define el espacio de nombres aquí

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    
    
    # # Asegúrate de incluir también las URLs para el proceso completo de restablecimiento
    # path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
