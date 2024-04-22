from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone
import requests
from django.core.files.base import ContentFile


def obtener_imagen_google_maps(latitud, 
                               longitud, 
                               label,
                               color,
                               lat_nominal=None, 
                               lon_nominal=None, 
                               lat_energia=None, 
                               lon_energia=None, 
                               zoom=18, 
                               maptype="hybrid", 
                               scale=2, 
                               tamano="640x400",
                               ):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    api_key = "AIzaSyD22EmbDEXIc7Meum5e2MCYj4D0JpDrmpU"


    # Verificar si lat_nominal y lon_nominal son válidos
    if lat_nominal in [None, ""] or lon_nominal in [None, ""]:
        centro = f"{latitud},{longitud}"
        if lat_energia in [None, ""] or lon_energia in [None, ""]:
            markers = [
                f"size:normal|color:{color}|label:{label}|{latitud},{longitud}",
                ]
        else:
            markers = [
                f"size:normal|color:{color}|label:{label}|{latitud},{longitud}",
                f"size:tiny|color:0x00FFFF|{lat_energia},{lon_energia}",
            ]
    else:
        # Si son válidos, calcular promedio para el centro y usar ambos para marcadores¡
        promedio_latitud = (latitud + lat_nominal) / 2
        promedio_longitud = (longitud + lon_nominal) / 2
        centro = f"{promedio_latitud},{promedio_longitud}"
        markers = [
            f"size:normal|color:0x00FF00|label:N|{lat_nominal},{lon_nominal}",
            f"size:mid|color:0xFFFF00|label:I|{latitud},{longitud}",
            f"size:tiny|color:0x00FFFF|{lat_energia},{lon_energia}",
        ]
    # print(imagen_content)
    params = {
        "center": centro,
        "zoom": zoom,
        "size": tamano,
        "maptype": maptype,  # "roadmap" Agrega este parámetro para obtener imágenes satelitales
        "scale" : scale,
        "key": api_key,
        "markers": markers,  # Agrega un marcador rojo con la etiqueta 'A'
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:

        return response.content
    else:
        return None


class Empresa(models.Model):
    pais = models.CharField(max_length=25)
    nombre = models.CharField(max_length=25)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
         
    def __str__(self):
        return f"{self.nombre} - {self.pais}"

class Sitio(models.Model):
    PTICellID = models.CharField("Cell ID", max_length=15)
    nombre = models.CharField(max_length=100, blank=True)
    lat_nominal = models.FloatField(blank=True, null=True, verbose_name='Latitud Nominal')
    lon_nominal = models.FloatField(blank=True, null=True, verbose_name='Longitud Nominal')
    altura = models.CharField(max_length=10, blank=True, null=True)
    provincia = models.CharField(max_length=25, blank=True, null=True)
    municipio = models.CharField(max_length=25, blank=True, null=True)
    localidad = models.CharField(max_length=25, blank=True, null=True)   
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, related_name='sitios', blank=True, null=True)
    
    img_google = models.ImageField(upload_to='imgs_gmap/', null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        print("==============")
        if not self.img_google:  # Si no hay imagen ya asociada, obten una nueva
            imagen_content = obtener_imagen_google_maps(
                self.lat_nominal, 
                self.lon_nominal, 
                label= "N",
                color="	#0f52ba",
                zoom=15
                )
            
            if imagen_content:
                filename = f"mapa_{self.pk or 'nuevo'}.png"
                self.img_google.save(filename, ContentFile(imagen_content), save=False)

        super(Sitio, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Sitio"
        verbose_name_plural = "Sitios"
        
    def __str__(self):
        return f"{self.PTICellID}"
    
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=120)
    telf = models.CharField(max_length=15)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    def __str__(self):
        return f"{self.user}"

class Candidato(models.Model):
    id = models.CharField(max_length=20, primary_key=True, blank=True)
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    candidato = models.IntegerField(validators=[MaxValueValidator(9)], default=1)
    fecha_creacion = models.DateTimeField("Fecha", auto_now_add=True)
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
 
    fecha_llegada = models.DateTimeField("Fecha de llegada", default=timezone.now)
    lat_llegada = models.FloatField(blank=True, null=True)
    lon_llegada = models.FloatField(blank=True, null=True)
    status_llegada = models.CharField("Estatus", max_length=10, choices=LLEGADA_CHOICES, default='ok')
    imagen_llegada = models.ImageField(upload_to='sitios/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.candidato.sitio}-{self.status_llegada}"
    
    class Meta:
        verbose_name = "Llegada Localidad"
        verbose_name_plural = "Llegada Localidad"

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
        verbose_name_plural = "Localidad"
    
class RegistroPropietario(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
    
    propietario_nombre_apellido = models.CharField('Nombre y Apellido',max_length=100)
    propietario_born = models.DateTimeField("Fecha de Nacimiento")
    propietario_ci = models.CharField("Documento de Identidad", max_length=15, blank=True, null=True)
    propietario_telf = models.CharField("Telefono de Contacto", max_length=15)
    propietario_direccion = models.TextField("Direccion Domicilio",max_length=100)
    propietario_estado_civil = models.BooleanField("Estado Civil",default=True)
    
    def __str__(self):
        return f"{self.propietario_nombre_apellido}"
    
    class Meta:
        verbose_name = "Propietario"
        verbose_name_plural = "Propietario"
   
class RegistroPropiedad(models.Model):
    candidato = models.OneToOneField(Candidato, on_delete=models.CASCADE)
        
    propiedad_rol = models.CharField("Rol",max_length=100)
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

    sitio_img_google = models.ImageField(upload_to='imgs_gmap/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        sitio = self.candidato.sitio  # Acceder al Sitio a través de Candidato
        latitud = sitio.lat_nominal  # Acceder a la latitud nominal
        longitud = sitio.lon_nominal  # Acceder a la longitud nominal
    
        if not self.sitio_img_google:  # Si no hay imagen ya asociada, obten una nueva
            imagen_content = obtener_imagen_google_maps(
                self.sitio_lat, 
                self.sitio_lon,
                label= "S",
                color="	red",
                lat_nominal=latitud,
                lon_nominal=longitud,
                zoom=15
                )
            
            if imagen_content:
                filename = f"mapa_{self.pk or 'nuevo'}.png"
                self.sitio_img_google.save(filename, ContentFile(imagen_content), save=False)

        super(RegistroSitio, self).save(*args, **kwargs)
        
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
    
    electrico_img_google = models.ImageField(upload_to='imgs_gmap/', null=True, blank=True)
    
    # def save(self, *args, **kwargs):
    #     id_candidato = self.candidato.pk
    #     registro_sitio = RegistroSitio.objects.get(pk=id_candidato)
    #     latitud_torre = registro_sitio.electrico_lat
    #     longitud_torre = registro_sitio.electrico_lon

        
    #     if not self.electrico_img_google:  # Si no hay imagen ya asociada, obten una nueva
    #         imagen_content = obtener_imagen_google_maps(
    #             self.electrico_lat, 
    #             self.electrico_lon,
    #             label= "S",
    #             color="	red",
    #             lat_nominal=latitud_torre,
    #             lon_nominal=longitud_torre,
    #             zoom=15
    #             )
            
    #         if imagen_content:
    #             filename = f"mapa_{self.pk or 'nuevo'}.png"
    #             self.electrico_img_google.save(filename, ContentFile(imagen_content), save=False)

    #     super(RegistroSitio, self).save(*args, **kwargs)