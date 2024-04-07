from rest_framework import serializers
from .models import RegistroCampo, Sitio
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitio
        fields = ['pais']


class RegistroCampoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroCampo
        fields = '__all__'
