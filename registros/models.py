from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone

class Servicio(models.Model):
    pais = models.CharField(max_length=25)
    empresa = models.CharField(max_length=25)
    
    class Meta:
        verbose_name_plural = "Pais Empresa"
         
    def __str__(self):
        return f"{self.pais} - {self.empresa}"

class Sitio(models.Model):
    pais_empresa = models.ForeignKey(Servicio, on_delete=models.SET_NULL, related_name='sitios', blank=True, null=True)
    PTICellID = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100, blank=True)
    lat_nominal = models.FloatField(blank=True, null=True, verbose_name='Latitud Nominal')
    lon_nominal = models.FloatField(blank=True, null=True, verbose_name='Longitud Nominal')
    altura = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f"{self.PTICellID}"
    
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telf = models.CharField(max_length=15)
    pais_empresa = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user}, {self.pais_empresa}"

LLEGADA_CHOICES = (
    ('ok', 'Llegada al lugar'),
    ('in', 'incidente'),
    ('no', 'No Llegada'),
)

class RegistroLlegada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='llegada_usuario')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name="llegada_sitio")
    candidato = models.IntegerField(validators=[MaxValueValidator(9)], default=1)
    
    fecha_llegada = models.DateTimeField()
    lat_llegada = models.FloatField(blank=True, null=True)
    lon_llegada = models.FloatField(blank=True, null=True)
    status_llegada = models.CharField("Llegada", max_length=10, choices=LLEGADA_CHOICES, default='ok')
    imagen_llegada = models.ImageField(upload_to='sitios/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.sitio}"
    
    class Meta:
        verbose_name = "Site Adquisition Report"
        verbose_name_plural = "Site Adquisition Report"



class RegistroLocalidad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='localidad_usuario')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name="localidad_sitio")
    candidato = models.ForeignKey(RegistroLlegada, on_delete=models.CASCADE, related_name="localidad_candidato")
    
    provincia = models.CharField(max_length=25, blank=True, null=True)
    municipio = models.CharField(max_length=25, blank=True, null=True)
    localidad = models.CharField(max_length=25, blank=True, null=True)
    energia_localidad = models.BooleanField(default=True)
    imagen_maps = models.ImageField(upload_to='sitios/gmaps', blank=True, null=True)

class RegistroPropietario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='propietario_usuario')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name="propietario_sitio")
    candidato = models.ForeignKey(RegistroLlegada, on_delete=models.CASCADE, related_name="propietario_candidato")
    
    propietario_nombre_apellido = models.CharField(max_length=100)
    propietario_born = models.DateTimeField()
    propietario_ci = models.CharField(max_length=15, blank=True, null=True)
    propietario_telf = models.CharField(max_length=15)
    propietario_direccion = models.TextField(max_length=100)
    propietario_estado_civil = models.BooleanField(default=True)
   
class RegistroPropiedad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='propiedad_usuario')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name="propiedad_sitio")
    candidato = models.ForeignKey(RegistroLlegada, on_delete=models.CASCADE, related_name="propiedad_candidato")
    
    propiedad_rol = models.CharField(max_length=100)
    propiedad_escritura = models.CharField(max_length=100)
    propiedad_registro_civil = models.TextField(max_length=100) 
    propiedad_imagen = models.ImageField(upload_to='sitios/', blank=True, null=True)
    propiedad_descripcion = models.TextField(blank=True, null=True)
    
class RegistroSitio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sitio_usuario')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name="sitio_sitio")
    candidato = models.ForeignKey(RegistroLlegada, on_delete=models.CASCADE, related_name="sitio_candidato")
    
    sitio_fecha = models.DateTimeField(default=timezone.now) 
    sitio_lat = models.FloatField(blank=True, null=True)
    sitio_lon = models.FloatField(blank=True, null=True)
    sitio_imagen = models.ImageField(upload_to='sitios/', blank=True, null=True)
    sitio_descripcion = models.TextField(blank=True, null=True)

class RegistroSitioImagenes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sitio_imagenes_usuario')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name="sitio_imagenes_sitio")
    candidato = models.ForeignKey(RegistroLlegada, on_delete=models.CASCADE, related_name="sitio_imagenes_candidato")
    
    pic = models.FileField(upload_to='fotografias/')
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    
class RegistioElectrico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='electrico_usuario')
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name="electrico_sitio")
    candidato = models.ForeignKey(RegistroLlegada, on_delete=models.CASCADE, related_name="electrico_candidato")
    
    electrico_lat = models.FloatField(blank=True, null=True)
    electrico_lon = models.FloatField(blank=True, null=True)
    electrico_no_poste = models.CharField(max_length=10, blank=True, null=True)
    electrico_comentario = models.TextField(blank=True, null=True)
    electrico_imagen1 = models.ImageField(upload_to='sitios/')
    electrico_imagen2 = models.ImageField(upload_to='sitios/', blank=True, null=True)