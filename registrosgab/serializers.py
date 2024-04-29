from rest_framework import serializers
from registros.models import RegistroPropietario    

class RegistroPropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroPropietario
        fields = '__all__'
