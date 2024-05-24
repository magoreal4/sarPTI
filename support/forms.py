# support/forms.py
from django import forms
from .models import SupportQuery

class SupportQueryForm(forms.ModelForm):
    class Meta:
        model = SupportQuery
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
