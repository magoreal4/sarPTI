from django.urls import path
from .views import policy_view, terms_view, file_list

app_name = 'configapp' 

urlpatterns = [
    path('policy-privacy/', policy_view, name='policy_view'),
    path('terms-conditions/', terms_view, name='terms_view'),
    path('files/', file_list, name='file_list'),

]
