from django.db import models
from django.contrib.auth.models import User

class Sitio(models.Model):
    pais = models.CharField(max_length=25)
    PTICellID = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100, blank=True)
    lat_nominal = models.FloatField(blank=True, null=True, verbose_name='Latitud Mandato')
    lon_nominal = models.FloatField(blank=True, null=True, verbose_name='Longitud Mandato')
    altura = models.CharField(max_length=10, blank=True, null=True)
    empresa = models.CharField(max_length=25, blank=True, null=True)

LLEGADA_CHOICES = (
    ('ok', 'Llegada al lugar'),
    ('in', 'incidente'),
    ('no', 'No Llegada'),
)

class Registro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Usuario')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name="sitios")
    fecha = models.DateTimeField()
    lat_llegada = models.FloatField(blank=True, null=True)
    lon_llegada = models.FloatField(blank=True, null=True)
    status_llegada = models.CharField("Llegada", max_length=10, choices=LLEGADA_CHOICES, default='ok')
    imagen_llegada = models.ImageField(upload_to='sitios/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    