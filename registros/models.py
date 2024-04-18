from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone

class Empresa(models.Model):
    pais = models.CharField(max_length=25)
    nombre = models.CharField(max_length=25)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "1. Empresas"
         
    def __str__(self):
        return f"{self.pais} - {self.nombre}"

class Sitio(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, related_name='sitios', blank=True, null=True)
    PTICellID = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100, blank=True)
    lat_nominal = models.FloatField(blank=True, null=True, verbose_name='Latitud Nominal')
    lon_nominal = models.FloatField(blank=True, null=True, verbose_name='Longitud Nominal')
    altura = models.CharField(max_length=10, blank=True, null=True)
    provincia = models.CharField(max_length=25, blank=True, null=True)
    municipio = models.CharField(max_length=25, blank=True, null=True)
    localidad = models.CharField(max_length=25, blank=True, null=True)   
    
    class Meta:
        verbose_name = "Sitio"
        verbose_name_plural = "3. Sitios"
        
    def __str__(self):
        return f"{self.PTICellID}"
    
    # class Meta:
#     verbose_name = "Site Adquisition Report"
#     verbose_name_plural = "Site Adquisition Report"
    
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telf = models.CharField(max_length=15)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "2. Usuarios"
    def __str__(self):
        return f"{self.user}"

class Candidato(models.Model):
    id = models.CharField(max_length=20, primary_key=True, blank=True)
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    candidato = models.IntegerField(validators=[MaxValueValidator(9)], default=1)

    def generate_id(self):
        # Genera el ID utilizando información del sitio y el número de candidato
        # pticell_suffix = self.sitio.PTICellID[-4:]
        return f"{self.sitio.PTICellID}_{self.candidato}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = self.generate_id()
        super(Candidato, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Registro Campo"
        verbose_name_plural = "Registros Campo"
        
LLEGADA_CHOICES = (
    ('ok', 'Llegada al lugar'),
    ('in', 'incidente'),
    ('no', 'No Llegada'),
)

class RegistroLlegada(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
 
    fecha_llegada = models.DateTimeField(default=timezone.now)
    lat_llegada = models.FloatField(blank=True, null=True)
    lon_llegada = models.FloatField(blank=True, null=True)
    status_llegada = models.CharField("Llegada", max_length=10, choices=LLEGADA_CHOICES, default='ok')
    imagen_llegada = models.ImageField(upload_to='sitios/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.candidato.sitio}-{self.status_llegada}"

class RegistroLocalidad(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
    
    provincia = models.CharField(max_length=25, blank=True, null=True)
    municipio = models.CharField(max_length=25, blank=True, null=True)
    localidad = models.CharField(max_length=25, blank=True, null=True)
    energia_localidad = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provincia}"
    
    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"
    
class RegistroPropietario(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
    
    propietario_nombre_apellido = models.CharField(max_length=100)
    propietario_born = models.DateTimeField("Fecha de Nacimiento")
    propietario_ci = models.CharField("Documento de Identidad", max_length=15, blank=True, null=True)
    propietario_telf = models.CharField("Telefono de Contacto", max_length=15)
    propietario_direccion = models.TextField("Direccion Domicilio",max_length=100)
    propietario_estado_civil = models.BooleanField("Casado",default=True)
    
    def __str__(self):
        return f"{self.propietario_nombre_apellido}"
    
    class Meta:
        verbose_name = "Propietario"
        verbose_name_plural = "Propietarios"
   
class RegistroPropiedad(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
        
    propiedad_rol = models.CharField(max_length=100)
    propiedad_escritura = models.CharField("Escritura", max_length=100)
    propiedad_registro_civil = models.TextField("Registro Civil",max_length=100) 
    propiedad_imagen = models.ImageField(upload_to='sitios/', blank=True, null=True)
    propiedad_descripcion = models.TextField("Comentarios",blank=True, null=True)
    
    def __str__(self):
        return f"Rol {self.propiedad_rol}"
    
    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"
        
class RegistroSitio(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
    
    sitio_fecha = models.DateTimeField("Fecha de Visita", default=timezone.now) 
    sitio_lat = models.FloatField("Latitud Torre", blank=True, null=True)
    sitio_lon = models.FloatField("Longitud Torre", blank=True, null=True)
    sitio_imagen = models.ImageField(upload_to='sitios/', blank=True, null=True)
    sitio_descripcion = models.TextField("Comentarios",blank=True, null=True)

    # def __str__(self):
    #     return f"{self.sitio}"
    
    class Meta:
        verbose_name = "Registro Sitio"
        verbose_name_plural = "Registro Sitios"
        
class RegistroSitioImagenes(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    
    pic = models.FileField(upload_to='fotografias/')
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.descripcion}"
    
    class Meta:
        verbose_name = "Imagen Sitio"
        verbose_name_plural = "Imagenes Sitios"
        
class RegistioElectrico(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
    
    electrico_lat = models.FloatField("Latitud Poste", blank=True, null=True)
    electrico_lon = models.FloatField("Longitud Poste", blank=True, null=True)
    electrico_no_poste = models.CharField("Identificacion Poste",max_length=10, blank=True, null=True)
    electrico_comentario = models.TextField("Comentario", blank=True, null=True)
    electrico_imagen1 = models.ImageField("Imagen Poste",upload_to='sitios/')
    electrico_imagen2 = models.ImageField("Imagen Electrico",upload_to='sitios/', blank=True, null=True)