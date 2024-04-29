from django.urls import path
from .views import (
    GetRegistroPropietario
    )

urlpatterns = [
    path('api/propietario/<str:pk>/', GetRegistroPropietario.as_view(), name='get_registro_propietario'),
]



