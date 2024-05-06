from django import forms
from django.contrib.auth.models import User

from .models import UserProfile  


class ProfileForm(forms.ModelForm):
    username = forms.CharField(required=False, max_length=150)
    password = forms.CharField(required=False, max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'password',)