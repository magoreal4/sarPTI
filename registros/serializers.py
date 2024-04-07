from rest_framework import serializers
from .models import RegistroCampo, Sitio
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# class SitioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sitio
#         fields = '__all__'

# class RegistroCampoSerializer(serializers.ModelSerializer):
#     usuario_id = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), write_only=True, source='usuario')
#     sitio_id = serializers.PrimaryKeyRelatedField(
#         queryset=Sitio.objects.all(), write_only=True, source='sitio')

#     usuario = UserSerializer(read_only=True)
#     sitio = SitioSerializer(read_only=True)

#     class Meta:
#         model = RegistroCampo
#         fields = '__all__'

#     def create(self, validated_data):
#         return RegistroCampo.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         # Aquí, actualizarías `instance` con `validated_data` y luego llamarías a `instance.save()`
#         # Por simplicidad, este paso se omite en el ejemplo.
#         return super().update(instance, validated_data)


class RegistroCampoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroCampo
        fields = '__all__'
