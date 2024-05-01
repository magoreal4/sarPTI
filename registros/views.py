from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

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
from main.models import UserProfile, Sitio


from .models import (
    RegistroLlegada,
    RegistroLocalidad,
    RegistroPropietario,
    RegistroPropiedad,
    RegistroSitio,
    RegistroSitioImagenes,
    RegistioElectrico
    )

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        token = None
        if user is not None:
            try:
                # Busca la instancia de Usuario relacionada con el usuario autenticado
                usuario = UserProfile.objects.get(user=user)
                # Ahora, accedemos al ID de pais_empresa directamente
                empresa_id = usuario.empresa.id
                mensaje = "Usuario logueado correctamente."
                token, _ = Token.objects.get_or_create(user=user)
            except UserProfile.DoesNotExist:
                # Maneja el caso en que no se encuentre una instancia de Usuario
                empresa_id = "None"  # O maneja este caso como prefieras
                mensaje = "Contactese con el administrador."

            data = {
                'user_id': user.id,
                'empresa_id': empresa_id,  # Devuelve el ID de pais_empresa
                'token': token.key,
            }
            return Response({"success": True, "data": data, "message": mensaje}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "error": {"message": "Credenciales inválidas."}}, status=status.HTTP_400_BAD_REQUEST)


class SitioListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, empresa_id):
        user = request.user
        sitios = Sitio.objects.filter(empresa_id=empresa_id, usuario=user)
        serializer = SitioSerializer(sitios, many=True)
        return Response(serializer.data)


class RegistroLlegadaList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        registros = RegistroLlegada.objects.all()
        serializer = RegistroLlegadaSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RegistroLlegadaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistroLocalidadList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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