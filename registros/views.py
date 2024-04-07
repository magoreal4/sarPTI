from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

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
