from django.urls import path
from .views import support_view, support_success

app_name = 'support'

urlpatterns = [
    path('', support_view, name='support_form'),
    path('success/', support_success, name='support_success'),
]
