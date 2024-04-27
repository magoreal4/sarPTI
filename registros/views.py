from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .serializers import (
    SitioSerializer,
    RegistroLlegadaSerializer, 
    RegistroLocalidadSerializer, 
    RegistroPropietarioSerializer, 
    RegistroPropiedadSerializer, 
    RegistroSitioSerializer,
    RegistroSitioImagenesSerializer, 
    RegistioElectricoSerializer
    )

from .models import (
    UserProfile,
    Sitio,
    RegistroLlegada, 
    RegistroLocalidad,
    RegistroPropietario,
    RegistroPropiedad,
    RegistroSitio,
    RegistroSitioImagenes,
    RegistioElectrico
    )

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                # Busca la instancia de Usuario relacionada con el usuario autenticado
                usuario = UserProfile.objects.get(user=user)
                # Ahora, accedemos al ID de pais_empresa directamente
                empresa_id = usuario.empresa.id
                mensaje = "Usuario logueado correctamente."
            except UserProfile.DoesNotExist:
                # Maneja el caso en que no se encuentre una instancia de Usuario
                empresa_id = "None"  # O maneja este caso como prefieras
                mensaje = "Contactese con el administrador."
                
            data = {
                'user_id': user.id,
                'empresa_id': empresa_id,  # Devuelve el ID de pais_empresa
            }
            return Response({"success": True, "data": data, "message": mensaje}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "error": {"message": "Credenciales inválidas."}}, status=status.HTTP_400_BAD_REQUEST)


class SitioListView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, empresa_id):
        sitios = Sitio.objects.filter(empresa_id=empresa_id)
        serializer = SitioSerializer(sitios, many=True)
        return Response(serializer.data)


class RegistroLlegadaList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        registros = RegistroLlegada.objects.all()
        serializer = RegistroLlegadaSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RegistroLlegadaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
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
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)