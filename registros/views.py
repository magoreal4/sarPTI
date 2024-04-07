from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import RegistroCampo
from .serializers import RegistroCampoSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Sitio

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

class ListaPaises(APIView):
    """
    Vista para listar todos los países únicos.
    """
    def get(self, request, format=None):
        # Obtener todos los países únicos
        paises = Sitio.objects.values_list('pais', flat=True).distinct()
        paises_lista = list(paises)
        return Response(paises_lista)


class RegistroCampoList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, format=None):
        registros = RegistroCampo.objects.all()
        serializer = RegistroCampoSerializer(registros, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RegistroCampoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
