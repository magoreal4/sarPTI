from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'main' 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

]
