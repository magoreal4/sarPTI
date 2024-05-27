from django.urls import path
from .views import policy_view, terms_view

app_name = 'configapp' 

urlpatterns = [
    path('policy-privacy/', policy_view, name='policy_view'),
    path('terms-conditions/', terms_view, name='terms_view'),

]
