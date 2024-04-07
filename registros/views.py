from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_tracking.mixins import LoggingMixin

class LoginAPIView( APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'token_type': 'Bearer',
                'expires_in': 3600,  # Tiempo de expiración en segundos, ejemplo
                'user_id': user.id,  # Información adicional como ID de usuario
                # Otros campos que consideres necesarios
            }
            return Response({"success": True, "data": data, "message": "Usuario logueado correctamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "error": {"message": "Credenciales inválidas."}}, status=status.HTTP_400_BAD_REQUEST)
