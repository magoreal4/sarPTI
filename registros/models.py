from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import requests
from django.core.files.base import ContentFile
from django.db import transaction
from django.db import IntegrityError
from geopy.distance import geodesic
from django.utils.html import format_html
from configapp.models import SiteConfiguration

def calcular_distancia_geopy(lat_1, lon_1, lat_2, lon_2):
    """Calcula la distancia entre dos puntos usando geopy."""
    if lat_1 is not None and lon_1 is not None and lat_2 is not None and lon_2 is not None:
        origen_coords = (lat_1, lon_1)
        destino_coords = (lat_2, lon_2)
        # Calcula la distanciroa usando geodesic de geopy
        distancia = geodesic(origen_coords, destino_coords).meters
        return distancia
    else:
        return None


def use_api_key():
    # Obtener la configuración del sitio
    try:
        config = SiteConfiguration.objects.get()
        api_key = config.api_key
        if api_key in [None, ""]:  # Verificar si la api_key es nula o vacía
            raise ValueError("API key is missing or invalid")
        return api_key
    except SiteConfiguration.DoesNotExist:
        raise ValueError("Site configuration is missing")

def get_google_maps(
        lat1,
        lon1,
        label1="N",
        color1="0E46A3",
        lat2=None,
        lon2=None,
        label2=None,
        color2=None,
        zoom=18,
        maptype="hybrid",
        scale=2,
        tamano="640x400",
):
    try:
        api_key = use_api_key()
    except ValueError as e:
        return str(e)  # Devuelve el mensaje de error si la api_key no está disponible

    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    # Verificar si lat_nominal y lon_nominal son válidos
    if lat2 in [None, ""] or lon2 in [None, ""]:
        centro = f"{lat1},{lon1}"
        markers = [
            f"size:normal|color:0x{color1}|label:{label1}|{lat1},{lon1}",
        ]
    else:
        promedio_lat = (lat1 + lat2) / 2
        promedio_lon = (lon1 + lon2) / 2
        centro = f"{promedio_lat},{promedio_lon}"
        markers = [
            f"size:normal|color:0x{color1}|label:{label1}|{lat1},{lon1}",
            f"size:mid|color:0x{color2}|label:{label2}|{lat2},{lon2}",
        ]
    params = {
        "center": centro,
        "zoom": zoom,
        "size": tamano,
        "maptype": maptype,
        "scale": scale,
        "key": api_key,
        "markers": markers,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.content
    else:
        return None



def ajustar_zoom(distancia):
    """
    Ajusta el nivel de zoom de Google Maps según la distancia dada para asegurar que
    toda la distancia pueda ser visualizada en la imagen.

    Parámetros:
    - distancia (float): La distancia en metros que se desea visualizar en la imagen.

    Retorna:
    - int: El nivel de zoom adecuado para Google Maps.
    """
    # Define los umbrales de distancia para cada nivel de zoom.
    # Estos valores son ejemplos y pueden ser ajustados según tus necesidades o pruebas
    if distancia <= 40:
        z = 20  # Aproximadamente 10 metros de ancho visible en el ecuador
    elif distancia <= 80:
        z = 19  # Aproximadamente 20 metros de ancho visible en el ecuador
    elif distancia <= 150:
        z = 18  # Aproximadamente 39 metros de ancho visible en el ecuador
    elif distancia <= 300:
        z = 17  # Aproximadamente 78 metros de ancho visible en el ecuador
    elif distancia <= 600:
        z = 16  # Aproximadamente 156 metros de ancho visible en el ecuador
    elif distancia <= 1300:
        z = 15  # Aproximadamente 313 metros de ancho visible en el ecuador
    elif distancia <= 2600:
        z = 14  # Aproximadamente 625 metros de ancho visible en el ecuador
    elif distancia <= 5300:
        z = 13  # Aproximadamente 1250 metros de ancho visible en el ecuador
    elif distancia <= 10000:
        z = 12  # Aproximadamente 2500 metros de ancho visible en el ecuador
    else:
        z = 11  # Aproximadamente 5000 metros de ancho visible en el ecuador

    return z


class Candidato(models.Model):
    sitio = models.ForeignKey('main.Sitio', on_delete=models.CASCADE)
    candidato = models.CharField(
        max_length=15,
        primary_key=True,  # Establece como clave primaria
        null=False,
        blank=True,
        verbose_name="Registro",
    )

    fecha_creacion = models.DateTimeField("Fecha", null=True, auto_now_add=True)

    def get_user_profile_info(self):
        # Asegúrate de que existe un UserProfile asociado al usuario
        if hasattr(self.usuario, 'userprofile'):
            return {
                'telefono': self.usuario.userprofile.telf,
                'empresa': self.usuario.userprofile.empresa
            }
        return None

    def save(self, *args, **kwargs):
        if not self.pk:  # Comprobar si es una nueva instancia
            with transaction.atomic():
                self.sitio.contador_llegadas += 1
                self.sitio.save()
                # Formato del identificador del candidato como 'brraabjo{PTICellID}{contador_llegadas}'
                self.candidato = f"{self.sitio.pk}_{self.sitio.contador_llegadas}"

        try:
            super().save(*args, **kwargs)  # Guarda el objeto con el ID modificado
        except IntegrityError as e:
            print(f"Error de integridad: {e}")

    def __str__(self):
        return f"{self.candidato}"

    class Meta:
        verbose_name = "Registro Campo (Consolidado)"
        verbose_name_plural = "Registros Campo (Consolidado)"


LLEGADA_CHOICES = (
    ('true', 'Llegada'),
    ('false', 'Incidente'),
)


class RegistroLlegada(models.Model):
    candidato = models.OneToOneField(
        Candidato,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    fecha_llegada = models.DateTimeField("Fecha de llegada", default=timezone.now)
    lat_llegada = models.FloatField("Latitud Llegada", null=True)
    lon_llegada = models.FloatField("Longitud Llegada", null=True)
    status_llegada = models.CharField("Estatus", choices=LLEGADA_CHOICES, max_length=5)
    imagen_llegada = models.ImageField(upload_to='llegada/', blank=True, null=True)
    observaciones = models.TextField(null=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        sitio = self.candidato.sitio
        if not sitio.img_google:  # Verifica si la imagen no existe en el modelo Sitio
            imagen_content = get_google_maps(
                sitio.lat_nominal, 
                sitio.lon_nominal, 
                zoom=15  # Ajustar el zoom según sea necesario
            )
            if imagen_content:
                filename = f"{sitio.PTICellID}_nominal.png"
                sitio.img_google.save(filename, ContentFile(imagen_content), save=True)  # Guarda la imagen en el modelo Sitio
        
        super(RegistroLlegada, self).save(*args, **kwargs) 
        
    def image_tag(self):
        return format_html('<img src="{}" width="150" height="auto"/>', self.imagen_llegada.url)
    image_tag.short_description = 'Imagen llegada'
    # image_tag.allow_tags = True

    def __str__(self):
        return f"{self.candidato}"

    class Meta:
        verbose_name = "Llegada"
        verbose_name_plural = "Llegada"


class RegistroLocalidad(models.Model):
    sitio = models.ForeignKey('main.Sitio', on_delete=models.CASCADE)
    candidato = models.OneToOneField(
        Candidato,
        on_delete=models.CASCADE,
        primary_key=True,
        blank=True,
        verbose_name="Registro",
    )
    provincia = models.CharField("Provincia/Region",max_length=35, blank=True, null=True)
    municipio = models.CharField("Municipio/Comuna",max_length=35, blank=True, null=True)
    localidad = models.CharField(max_length=25, blank=True, null=True)
    energia_localidad = models.BooleanField(default=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # Comprobar si es una nueva instancia
            candidato_id = f"{self.sitio.pk}_{self.sitio.contador_llegadas}"
            candidato, created = Candidato.objects.get_or_create(
                candidato=candidato_id,
                defaults={'sitio': self.sitio}
            )
            self.candidato = candidato
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            print(f"Error de integridad: {e}")

    def __str__(self):
        return f"{self.provincia}"

    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidad"

TIPO_PERSONA = (
    ('natural', 'Natural'),
    ('juridica', 'Juridica'),
)

class RegistroPropietario(models.Model):
    sitio = models.ForeignKey('main.Sitio', on_delete=models.CASCADE)
    candidato = models.OneToOneField(
        Candidato,
        on_delete=models.CASCADE,
        primary_key=True,
        blank=True,
        verbose_name="Registro",
    )
    # Version 1.2
    propietario_tipo_persona = models.CharField("Tipo de Persona", choices=TIPO_PERSONA, max_length=8, default='natural' )
    
    propietario_nombre_apellido = models.CharField('Nombre y Apellido', max_length=100)
    propietario_born = models.DateTimeField("Fecha de Nacimiento")
    propietario_ci = models.CharField("Documento de Identidad", max_length=15, blank=True, null=True)
    propietario_telf = models.CharField("Telefono de Contacto", max_length=15)
    propietario_direccion = models.TextField("Direccion Domicilio", max_length=100)
    propietario_estado_civil = models.BooleanField("Estado Civil", default=True)
    
    # Version 1.1
    propietario_email = models.EmailField("Correo electronico", max_length=100, blank=True, null=True)
    contacto_nombre = models.CharField("Nombre de Contacto", max_length=100, blank=True, null=True)
    contacto_tel = models.CharField("Telefono de Contacto", max_length=15, blank=True, null=True)
    contacto_email = models.EmailField("Email de Contacto", max_length=100, blank=True, null=True)
    contacto_relacion = models.CharField("Relacion con Propietario", max_length=100, blank=True, null=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Comprobar si es una nueva instancia
            candidato_id = f"{self.sitio.pk}_{self.sitio.contador_llegadas}"
            candidato, created = Candidato.objects.get_or_create(
                candidato=candidato_id,
                defaults={'sitio': self.sitio}
            )
            self.candidato = candidato
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            print(f"Error de integridad: {e}")

    def __str__(self):
        return f"{self.propietario_nombre_apellido}"

    class Meta:
        verbose_name = "Propietario"
        verbose_name_plural = "Propietario"


class RegistroPropiedad(models.Model):
    sitio = models.ForeignKey('main.Sitio', on_delete=models.CASCADE)
    candidato = models.OneToOneField(
        Candidato,
        on_delete=models.CASCADE,
        primary_key=True,
        blank=True,
        verbose_name="Registro",
    )

    propiedad_rol = models.CharField("Rol", max_length=100)
    propiedad_escritura = models.CharField("Escritura", max_length=100)
    propiedad_registro_civil = models.TextField("Registro Civil", max_length=100)
    propiedad_imagen = models.ImageField(upload_to='sitios/propiedad',null=True)
    propiedad_descripcion = models.TextField("Comentarios")
    
    # Version 1.1
    propiedad_direccion = models.CharField("Direccion Propiedad", max_length=100, null=True, blank=True)
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def image_tag(self):
        return format_html('<img src="{}" width="150" height="auto"/>', self.propiedad_imagen.url)

    image_tag.short_description = 'Imagen Propiedad'

    def save(self, *args, **kwargs):
        if not self.pk:  # Comprobar si es una nueva instancia
            candidato_id = f"{self.sitio.pk}_{self.sitio.contador_llegadas}"
            candidato, created = Candidato.objects.get_or_create(
                candidato=candidato_id,
                defaults={'sitio': self.sitio}
            )
            self.candidato = candidato
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError as e:
            # Ahora lanzamos la excepción para que pueda ser capturada por la vista
            raise ValueError(f"Error de integridad: {e}")

    def __str__(self):
        return f"Rol {self.propiedad_rol}"

    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedad"


class RegistroSitio(models.Model):
    sitio = models.ForeignKey('main.Sitio', on_delete=models.CASCADE)
    candidato = models.OneToOneField(
        Candidato,
        on_delete=models.CASCADE,
        primary_key=True,
        blank=True,
        verbose_name="Registro",
    )

    sitio_fecha = models.DateTimeField("Fecha de Visita")
    sitio_lat = models.FloatField("Latitud Torre")
    sitio_lon = models.FloatField("Longitud Torre")
    sitio_descripcion = models.TextField("Comentarios")
    
    # Version 1.1
    sitio_propuesta_negociacion = models.CharField("Propuesta de Negociación", max_length=100, null=True)
    sitio_espacio_negociado = models.CharField("Espacio Negociado", max_length=100, null=True)  

    img_google_dist_nominal = models.ImageField(upload_to='sitios/imgs_gmap/', null=True, blank=True)
    img_google_sitio = models.ImageField(upload_to='sitios/imgs_gmap/', null=True, blank=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Crear el pk de candidato
        if not self.pk:
            candidato_id = f"{self.sitio.pk}_{self.sitio.contador_llegadas}"
            candidato, created = Candidato.objects.get_or_create(
                candidato=candidato_id,
                defaults={'sitio': self.sitio}
            )
            self.candidato = candidato

        # Imagen satelital
        sitio = self.candidato.sitio  # Acceder al Sitio a través de Candidato
        lat_N = sitio.lat_nominal  # Acceder a la latitud nominal
        lon_N = sitio.lon_nominal  # Acceder a la longitud nominal

        distancia = calcular_distancia_geopy(
            lat_N, lon_N, self.sitio_lat, self.sitio_lon
        )

        if not self.img_google_dist_nominal:
            z = ajustar_zoom(distancia)

            imagen_content = get_google_maps(
                lat_N,
                lon_N,
                lat2=self.sitio_lat,
                lon2=self.sitio_lon,
                label2="S",
                color2="41B06E",
                zoom=z
            )

            if imagen_content:
                filename = f"{self.pk or 'nuevo'}_dist_nominal.png"
                self.img_google_dist_nominal.save(filename, ContentFile(imagen_content), save=False)

        if not self.img_google_sitio:  # Si no hay imagen ya asociada, obten una nueva
            imagen_content = get_google_maps(
                self.sitio_lat,
                self.sitio_lon,
                label1="S",
                color1="41B06E",
                zoom=18
            )

            if imagen_content:
                filename = f"{self.pk or 'nuevo'}.png"
                self.img_google_sitio.save(filename, ContentFile(imagen_content), save=False)

        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValueError(f"Error de integridad: {e}")

    def image_tag_img_google_sitio(self):
        return format_html('<img src="{}" width="320" height="auto"/>', self.img_google_sitio.url)

    image_tag_img_google_sitio.short_description = 'Imagen Satelital Sitio'

    def image_tag_img_google_dist_nominal(self):
        return format_html('<img src="{}" width="320" height="auto"/>', self.img_google_dist_nominal.url)

    image_tag_img_google_dist_nominal.short_description = 'Imagen Satelital Distancia a Coordenadas nominales'

    def __str__(self):
        return f"{self.sitio}"

    class Meta:
        verbose_name = "Sitio"
        verbose_name_plural = "Sitio"


class RegistroSitioImagenes(models.Model):
    sitio = models.ForeignKey('main.Sitio', on_delete=models.CASCADE)
    candidato = models.ForeignKey(
        Candidato,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="Registro",
    )

    pic = models.FileField(upload_to='sitios/fotos/')
    descripcion = models.CharField(max_length=100, blank=True, null=True, default="---") 
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            candidato_id = f"{self.sitio.pk}_{self.sitio.contador_llegadas}"
            candidato, created = Candidato.objects.get_or_create(
                candidato=candidato_id,
                defaults={'sitio': self.sitio}
            )
            self.candidato = candidato
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValueError(f"Error de integridad: {e}")

    def __str__(self):
        return f"{self.descripcion}"

    def image_tag_pic(self):
        return format_html('<img src="{}" width="80" height="auto"/>', self.pic.url)

    image_tag_pic.short_description = 'Imagen Sitio'

    class Meta:
        verbose_name = "Imagen Sitio"
        verbose_name_plural = "Imagenes Sitio"


class RegistioElectrico(models.Model):
    sitio = models.ForeignKey('main.Sitio', on_delete=models.CASCADE)
    candidato = models.OneToOneField(
        Candidato,
        on_delete=models.CASCADE,
        primary_key=True,
        blank=True,
        verbose_name="Registro",
    )

    electrico_lat = models.FloatField("Latitud Poste")
    electrico_lon = models.FloatField("Longitud Poste")
    electrico_no_poste = models.CharField("Identificacion Poste", max_length=10, blank=True, null=True)
    electrico_comentario = models.TextField("Comentario", blank=True, null=True, default="Sin Comentario")
    electrico_imagen1 = models.ImageField("Imagen Poste", upload_to='sitios/')
    electrico_imagen2 = models.ImageField("Imagen Electrico", upload_to='sitios/', blank=True, null=True)

    electrico_img_google = models.ImageField(upload_to='sitios/imgs_gmap/', null=True, blank=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            candidato_id = f"{self.sitio.pk}_{self.sitio.contador_llegadas}"
            candidato, created = Candidato.objects.get_or_create(
                candidato=candidato_id,
                defaults={'sitio': self.sitio}
            )
            self.candidato = candidato

        def get_sitio_coordinates(self):
            try:
                # Asumiendo que el modelo Candidato tiene un atributo 'registrositio'
                registro_sitio = self.candidato.registrositio
                return registro_sitio.sitio_lat, registro_sitio.sitio_lon
            except AttributeError:
                # Manejar el caso donde 'registrositio' no está disponible
                return None, None
            except Candidato.DoesNotExist:
                # Manejar el caso donde no hay un objeto Candidato asociado
                return None, None
            except Exception as e:
                # Manejar cualquier otra excepción que podría ocurrir
                print(f"Error al obtener las coordenadas del sitio: {e}")
                return None, None

        lat, lon = get_sitio_coordinates(self)

        if not self.electrico_img_google:  # Si no hay imagen ya asociada, obten una nueva

            distancia = calcular_distancia_geopy(
                lat, lon, self.electrico_lat, self.electrico_lon)
            z = ajustar_zoom(distancia)

            imagen_content = get_google_maps(
                lat,
                lon,
                label1="S",
                color1="41B06E",
                zoom=z,
                lat2=self.electrico_lat,
                lon2=self.electrico_lon,
                label2="E",
                color2="FF6500",
            )

            if imagen_content:
                filename = f"{self.pk or 'nuevo'}_dist_electrico.png"
                self.electrico_img_google.save(filename, ContentFile(imagen_content), save=False)

        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValueError(f"Error de integridad: {e}")

    class Meta:
        verbose_name = "Eléctrico"
        verbose_name_plural = "Eléctrico"
 