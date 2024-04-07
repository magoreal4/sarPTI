from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
# from .models import RegistroLocalidad
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    RegistroLlegadaSerializer, 
    RegistroLocalidadSerializer, 
    RegistroPropietarioSerializer, 
    RegistroPropiedadSerializer, 
    RegistroSitioSerializer,
    RegistroSitioImagenesSerializer, 
    RegistioElectricoSerializer
    )

from .models import (
    RegistroLlegada, 
    RegistroLocalidad,
    RegistroPropietario,
    RegistroPropiedad,
    RegistroSitio,
    RegistroSitioImagenes,
    RegistioElectrico
    )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Aquí simplemente devolvemos una respuesta de éxito sin generar tokens
            data = {
                'user_id': user.id,  # Aún puedes optar por devolver el ID del usuario o cualquier otra información necesaria
                # Otros campos que consideres necesarios
            }
            return Response({"success": True, "data": data, "message": "Usuario logueado correctamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "error": {"message": "Credenciales inválidas."}}, status=status.HTTP_400_BAD_REQUEST)

class RegistroLlegadaList(APIView):
    """
    Lista todos los registros de llegada o crea un nuevo registro.
    """
    def get(self, request, format=None):
        registros = RegistroLlegada.objects.all()
        serializer = RegistroLlegadaSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistroLlegadaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistroLocalidadList(APIView):
    """
    Lista todos los registros de localidad o crea un nuevo registro.
    """
    def get(self, request, format=None):
        registros = RegistroLocalidad.objects.all()
        serializer = RegistroLocalidadSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistroLocalidadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegistroPropietarioList(APIView):
    """
    Lista todos los registros de propietario o crea un nuevo registro.
    """
    def get(self, request, format=None):
        registros = RegistroPropietario.objects.all()
        serializer = RegistroPropietarioSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistroPropietarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegistroPropiedadList(APIView):
    """
    Lista todos los registros de propiedad o crea un nuevo registro.
    """
    def get(self, request, format=None):
        registros = RegistroPropiedad.objects.all()
        serializer = RegistroPropiedadSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistroPropiedadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistroSitioList(APIView):
    """
    Lista todos los registros de sitio o crea un nuevo registro.
    """
    def get(self, request, format=None):
        registros = RegistroSitio.objects.all()
        serializer = RegistroSitioSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistroSitioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class RegistroSitioImagenesList(APIView):
    """
    Lista todos los registros de sitio o crea un nuevo registro.
    """
    def get(self, request, format=None):
        registros = RegistroSitioImagenes.objects.all()
        serializer = RegistroSitioImagenesSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistroSitioImagenesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class RegistioElectricoList(APIView):
    """
    Lista todos los registros de electrico o crea un nuevo registro.
    """
    def get(self, request, format=None):
        registros = RegistioElectrico.objects.all()
        serializer = RegistioElectricoSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistioElectricoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ListaPaises(APIView):
#     """
#     Vista para listar todos los países únicos.
#     """
#     def get(self, request, format=None):
#         # Obtener todos los países únicos
#         paises = Sitio.objects.values_list('pais', flat=True).distinct()
#         paises_lista = list(paises)
#         return Response(paises_lista)