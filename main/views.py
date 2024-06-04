from django.views.generic import TemplateView
# from .models import PolicyDocument
from django.shortcuts import render

class Home(TemplateView):
    template_name = "home_page.html"
    
