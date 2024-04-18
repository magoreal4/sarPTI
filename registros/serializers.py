from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Sitio,
    Candidato,
    RegistroLlegada, 
    RegistroLocalidad,
    RegistroPropietario,
    RegistroPropiedad,
    RegistroSitio,
    RegistroSitioImagenes,
    RegistioElectrico,
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class SitioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitio
        fields = '__all__'

class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidato
        fields = ['id', 'sitio', 'usuario', 'candidato']

class RegistroLlegadaSerializer(serializers.ModelSerializer): 
    candidato = CandidatoSerializer()
    class Meta:
        model = RegistroLlegada
        fields = ['candidato', 
                'fecha_llegada',
                'lat_llegada',
                'lon_llegada',
                'status_llegada',
                'imagen_llegada',
                'observaciones',
                ]

    def create(self, validated_data):
        candidato_data = validated_data.pop('candidato')
        candidato = Candidato.objects.create(**candidato_data)
        registro_llegada = RegistroLlegada.objects.create(candidato=candidato, **validated_data)
        return registro_llegada

    def update(self, instance, validated_data):
        candidato_data = validated_data.pop('candidato', None)
        if candidato_data:
            # Update the Candidato instance if necessary
            Candidato.objects.filter(id=instance.candidato.id).update(**candidato_data)

        # Update the RegistroLlegada instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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
