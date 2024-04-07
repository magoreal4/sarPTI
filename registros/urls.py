from django.urls import path
from .views import LoginAPIView, RegistroCampoList, ListaPaises

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/paises/', ListaPaises.as_view(), name='lista-paises'),
    path('api/registrocampo/', RegistroCampoList.as_view(), name='registrocampo'),
]
