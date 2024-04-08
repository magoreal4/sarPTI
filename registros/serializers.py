from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Sitio,
    RegistroLlegada, 
    RegistroLocalidad,
    RegistroPropietario,
    RegistroPropiedad,
    RegistroSitio,
    RegistioElectrico,
    RegistroSitioImagenes,
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class SitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitio
        fields = '__all__'

class RegistroLlegadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroLlegada
        fields = '__all__'

class RegistroLocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroLocalidad
        fields = '__all__'

class RegistroPropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroPropietario
        fields = '__all__'

class RegistroPropiedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroPropiedad
        fields = '__all__'
        
class RegistroSitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroSitio
        fields = '__all__'

class RegistroSitioImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroSitioImagenes
        fields = '__all__'


class RegistioElectricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistioElectrico
        fields = '__all__'
