from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroInicioForm
from .models import RegistroInicio

class RegistroInicioCreate(LoginRequiredMixin, CreateView):
    model = RegistroInicio
    form_class = RegistroInicioForm

    def get_form_kwargs(self):
        kwargs = super(RegistroInicioCreate, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegistroPropietario
from .serializers import RegistroPropietarioSerializer

class GetRegistroPropietario(APIView):
    def get(self, request, pk, format=None):
        try:
            registro = RegistroPropietario.objects.get(pk=pk)
            serializer = RegistroPropietarioSerializer(registro)
            return Response(serializer.data)
        except RegistroPropietario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
