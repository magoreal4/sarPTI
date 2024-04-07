from django.urls import path
from .views import LoginAPIView, RegistroCampoList

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/registrocampo/', RegistroCampoList.as_view(), name='registrocampo'),
]
