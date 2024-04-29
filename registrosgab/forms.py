from django import forms
from .models import RegistroInicio
from registros.models import RegistroLlegada

class RegistroInicioForm(forms.ModelForm):
    class Meta:
        model = RegistroInicio
        fields = [
            'candidato_letra', 
            'candidato_registro', 
            'radio_busqueda',
            'tipo_solucion',
            'zona',
            'ASNM',
            'contactos_ingreso',
            'ruta_acceso',
            'ruta_huella',
            'inf_adicional',
            # 'usuario'
            ]

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(RegistroInicioForm, self).__init__(*args, **kwargs)
        if user_id is not None:
            self.fields['candidato_registro'].queryset = RegistroLlegada.objects.filter(usuario__id=user_id)

    
    
    
    
    