from django import forms
from django.forms.widgets import TextInput
from .models import SiteConfiguration


class APIKeyWidget(TextInput):
    input_type = 'text'  # Cambiar a text

    def __init__(self, attrs=None):
        default_attrs = {'style': 'font-family: monospace; -webkit-text-security: disc;'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class ConfiguracionForm(forms.ModelForm):
    api_key = forms.CharField(widget=APIKeyWidget())

    class Meta:
        model = SiteConfiguration
        fields = ['api_key']
        labels = {
            'api_key': 'Clave API',
        }
        help_texts = {
            'api_key': 'Ingrese la clave API para configurar el sistema.',
        }
