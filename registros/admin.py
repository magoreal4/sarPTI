from django.contrib import admin
from django.db.models import F
import pytz
from main.models import Empresa, Sitio, UserProfile
from .models import (Candidato,
                     RegistroLlegada,
                     RegistroLocalidad,
                     RegistroPropietario,
                     RegistroPropiedad,
                     RegistroSitio,
                     RegistroSitioImagenes,
                     RegistioElectrico
                     )
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.formats import date_format
from django.utils.html import format_html
from geopy.distance import geodesic
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Buscador'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


def dec_to_gms(decimal_deg, is_lat=True):
    if decimal_deg is None or decimal_deg == "":
        return "-"
    # Determina si el grado es negativo (Sur o Oeste)
    is_negative = decimal_deg < 0
    # Convierte el grado a positivo para el cálculo
    decimal_deg = abs(decimal_deg)

    degrees = int(decimal_deg)
    minutes = int((decimal_deg - degrees) * 60)
    seconds = (decimal_deg - degrees - minutes / 60) * 3600.00

    # Decide el sufijo basado en si es latitud y si es positivo/negativo
    if is_lat:
        suffix = "S" if is_negative else "N"
    else:
        suffix = "O" if is_negative else "E"

    return f"{degrees}° {minutes}' {seconds:.2f}\" {suffix}"


def calcular_distancia_geopy(lat_1, lon_1, lat_2, lon_2):
    """Calcula la distancia entre dos puntos usando geopy."""
    if lat_1 is not None and lon_1 is not None and lat_2 is not None and lon_2 is not None:
        origen_coords = (lat_1, lon_1)
        destino_coords = (lat_2, lon_2)
        # Calcula la distancia usando geodesic de geopy
        distancia = geodesic(origen_coords, destino_coords).meters
        return distancia
    else:
        return None

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('pais', 'nombre')


admin.site.register(Empresa, EmpresaAdmin)


# SITIOS
class SitiosResource(resources.ModelResource):
    class Meta:
        model = Sitio
        import_id_fields = ('PTICellID',)


class SitioAdmin(ImportExportModelAdmin):
    list_display = ('PTICellID',
                    'nombre',
                    'altura',
                    'empresa',
                    'usuario',
                    'contador_llegadas',
                    # 'img_thumbnail'
                    )
    list_editable = ('empresa','usuario')
    readonly_fields = ['img_thumbnail']
    fields = (
        'PTICellID',
        'nombre',
        'lat_nominal',
        'lon_nominal',
        'altura',
        'provincia',
        'municipio',
        'localidad',
        'empresa',
        'usuario',
        # 'img_google',
        'contador_llegadas',
        'img_thumbnail'
    )
    # list_filter = ('empresa',)

    resource_class = SitiosResource
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('main.view_empresa_sites'):
            return qs
        if request.user.userprofile.empresa:
            return qs.filter(empresa=request.user.userprofile.empresa)
        return qs.none()

    def img_thumbnail(self, obj):
        if obj.img_google:
            return format_html('<img src="{}" width="320"  />', obj.img_google.url)
        else:
            return "No hay imagen"

    img_thumbnail.short_description = 'Ubicaion Preview'


admin.site.register(Sitio, SitioAdmin)


# REGISTRO LLEGADA
class RegistroLlegadaInline(admin.StackedInline):
    model = RegistroLlegada
    extra = 0
    readonly_fields = (
        'fecha_llegada_chile', 'status_llegada_text',
        'lat_llegada', 'lat_llegada_gms',
        'lon_llegada', 'lon_llegada_gms',
        'imagen_llegada_preview', 'observaciones',
    )
    fieldsets = (
        ('', {
            'fields': (
                ('fecha_llegada_chile', 'status_llegada_text',),
                ('lat_llegada', 'lat_llegada_gms',),
                ('lon_llegada', 'lon_llegada_gms',),
                ('imagen_llegada_preview', 'observaciones'),

            ),
        }),)

    def fecha_llegada_chile(self, obj):
        timezone_chile = pytz.timezone('America/Santiago')
        datetime_chile = obj.fecha_llegada.astimezone(timezone_chile)
        return date_format(datetime_chile, "d/m/Y  -  H:i")
    fecha_llegada_chile.short_description = "Fecha Llegada"
    
    def lat_llegada_gms(self, obj):
        return dec_to_gms(obj.lat_llegada)

    lat_llegada_gms.short_description = "Latitud Llegada (GMS)"

    def lon_llegada_gms(self, obj):
        return dec_to_gms(obj.lon_llegada)

    lon_llegada_gms.short_description = "Longitud Llegada (GMS)"

    def imagen_llegada_preview(self, obj):
        if obj.imagen_llegada:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.imagen_llegada.url)
        return "No hay imagen"

    imagen_llegada_preview.short_description = 'Imagen Localidad'

    def status_llegada_text(self, obj):
        if obj.status_llegada == "true":
            return format_html('<span style="color: green;">&#10003; Llegada Exitosa</span>')
        else:
            return format_html('<span style="color: red;">&#10005; No se llegó a la zona</span>')

    status_llegada_text.short_description = "Estatus"


class RegistroLlegadaAdmin(admin.ModelAdmin):
    ordering = ('-fecha_llegada',)
    list_display = ('candidato',
                    'usuario',
                    'status_llegada',
                    'fecha_llegada_chile',
                    # 'imagen_thumbnail',
                    )
    list_editable = ('status_llegada',)
    readonly_fields = ['image_tag', 'fecha_llegada_chile']
    fields = (
        'candidato', 'status_llegada', 'fecha_llegada_chile', 'lat_llegada', 'lon_llegada', 'observaciones', 'imagen_llegada',
        'image_tag')

    def fecha_llegada_chile(self, obj):
        timezone_chile = pytz.timezone('America/Santiago')
        datetime_chile = obj.fecha_llegada.astimezone(timezone_chile)
        return date_format(datetime_chile, "j F Y - H:i")
    fecha_llegada_chile.short_description = 'Fecha - Hora'
    fecha_llegada_chile.admin_order_field = 'fecha_llegada'
    
    def imagen_thumbnail(self, obj):
        if obj.imagen_llegada:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="160" height=""/>', obj.imagen_llegada.url)
        return "No hay imagen"
    imagen_thumbnail.short_description = 'Imagen Localidad'


admin.site.register(RegistroLlegada, RegistroLlegadaAdmin)


# REGISTRO LOCALIDAD
class RegistroLocalidadInline(admin.StackedInline):
    model = RegistroLocalidad
    extra = 0
    readonly_fields = ('provincia', 'municipio', 'localidad', 'energia_localidad_mensaje')
    fieldsets = (
        ('', {
            'fields': (
                ('provincia', 'municipio', 'localidad'),
                ('energia_localidad_mensaje')
            ),
        }),)

    def energia_localidad_mensaje(self, obj):
        if obj.energia_localidad:
            return "Cuenta con energía Electríca"
        else:
            return "No Cuenta con energía Electríca"

    energia_localidad_mensaje.short_description = "Energía Ecéctrica"


class RegistroLocalidadAdmin(admin.ModelAdmin):
    list_display = ('candidato',
                    'provincia',
                    'municipio',
                    'localidad',
                    'energia_localidad'
                    )
    list_editable = ('energia_localidad',)


admin.site.register(RegistroLocalidad, RegistroLocalidadAdmin)


# REGISTRO PROPIETARIO
class RegistroPropietariodInline(admin.StackedInline):
    model = RegistroPropietario
    extra = 0
    readonly_fields = ('propietario_nombre_apellido',
                       'fecha_nacimiento',
                       'propietario_ci',
                       'propietario_telf',
                       'propietario_direccion',
                       'propietario_estado_civil_mensaje',)
    fieldsets = (
        ('', {
            'fields': (
                ('propietario_nombre_apellido',),
                ('fecha_nacimiento', 'propietario_ci', 'propietario_telf'),
                ('propietario_direccion', 'propietario_estado_civil_mensaje'),
            ),
        }),)

    def propietario_estado_civil_mensaje(self, obj):
        if obj.propietario_estado_civil:
            return "Casado"
        else:
            return "Soltero"

    propietario_estado_civil_mensaje.short_description = "Estado Civil"

    def fecha_nacimiento(self, obj):
        return date_format(obj.propietario_born, "d/m/Y")

    fecha_nacimiento.short_description = 'Fecha de Nacimiento'


class RegistroPropietarioAdmin(admin.ModelAdmin):
    list_display = ('candidato',
                    'propietario_nombre_apellido',
                    'propietario_telf',
                    )
    fields = ('candidato',
              'propietario_nombre_apellido',
              'propietario_born',
              'propietario_estado_civil',
              'propietario_ci',
              'propietario_telf',
              'propietario_direccion',
              )

admin.site.register(RegistroPropietario, RegistroPropietarioAdmin)


# REGISTRO PROPIEDAD
class RegistroPropiedadInline(admin.StackedInline):
    model = RegistroPropiedad
    extra = 0
    readonly_fields = ('propiedad_rol', 'propiedad_escritura',
                       'propiedad_registro_civil',
                       'propiedad_imagen_thumbnail',
                       'propiedad_descripcion',)
    fieldsets = (
        ('', {
            'fields': (
                ('propiedad_rol', 'propiedad_escritura', 'propiedad_registro_civil'),
                ('propiedad_imagen_thumbnail', 'propiedad_descripcion'),
            ),
        }),)



    def propiedad_imagen_thumbnail(self, obj):
        if obj.propiedad_imagen:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.propiedad_imagen.url)
        return "No hay imagen"

    propiedad_imagen_thumbnail.short_description = 'Imagen Principal de la Propiedad'


class RegistroPropiedadAdmin(admin.ModelAdmin):
    list_display = ('candidato',
                    'propiedad_rol',
                    'propiedad_escritura',
                    'propiedad_registro_civil',
                    )
    # list_editable = ('status_llegada', )
    readonly_fields = ['image_tag']
    fields = ('candidato',
              'propiedad_rol',
              'propiedad_escritura',
              'propiedad_registro_civil',
              'propiedad_descripcion',
              'propiedad_imagen', 'image_tag',)


admin.site.register(RegistroPropiedad, RegistroPropiedadAdmin)


# REGISTRO SITIO
class RegistroSitioInline(admin.StackedInline):
    model = RegistroSitio
    extra = 0
    readonly_fields = ('sitio_fecha_chile',
                       'sitio_lat', 'sitio_lat_gms',
                       'sitio_lon', 'sitio_lon_gms',
                       'sitio_imagen_thumbnail',
                       'sitio_descripcion',
                       'img_google_distancia_nominal',
                       'distancia_coordenadas',
                       'img_google')
    fieldsets = (
        ('', {
            'fields': (
                'sitio_fecha_chile',
                ('sitio_lat', 'sitio_lat_gms'),
                ('sitio_lon', 'sitio_lon_gms'),
                ('img_google_distancia_nominal', 'sitio_descripcion'),
                ('distancia_coordenadas',),
                'img_google',
            ),
        }),)


    def sitio_fecha_chile(self, obj):
        timezone_chile = pytz.timezone('America/Santiago')
        datetime_chile = obj.sitio_fecha.astimezone(timezone_chile)
        return date_format(datetime_chile, "d/m/Y  -  H:i")
    sitio_fecha_chile.short_description = 'Fecha - Hora'

    def sitio_imagen_thumbnail(self, obj):
        if obj.sitio_imagen:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.sitio_imagen.url)
        return "No hay imagen"

    sitio_imagen_thumbnail.short_description = 'Imagen Principal del Sitio'

    def distancia_coordenadas(self, obj):
        if obj.sitio_lat:
            distancia = calcular_distancia_geopy(
                obj.sitio_lat,
                obj.sitio_lon,
                obj.candidato.sitio.lat_nominal,
                obj.candidato.sitio.lon_nominal
            )
            return f"{round(distancia, 2)} m"
        return "Sin distancia"

    distancia_coordenadas.short_description = 'Distancia a Coordenadas nominales'

    def img_google_distancia_nominal(self, obj):
        if obj.img_google_dist_nominal:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="420" height=""/>', obj.img_google_dist_nominal.url)
        return "No hay imagen"

    img_google_distancia_nominal.short_description = 'Imagen Satelital Distancia a Coordenadas nominales'

    def img_google(self, obj):
        if obj.img_google_sitio:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="480" height=""/>', obj.img_google_sitio.url)
        return "No hay imagen"

    img_google.short_description = 'Imagen Satelital Sitio'

    def sitio_lat_gms(self, obj):
        return dec_to_gms(obj.sitio_lat)

    sitio_lat_gms.short_description = "Latitud Torre (GMS)"

    def sitio_lon_gms(self, obj):
        return dec_to_gms(obj.sitio_lon)

    sitio_lon_gms.short_description = "Longitud Torre (GMS)"


class RegistroSitioAdmin(admin.ModelAdmin):
    ordering = ('-sitio_fecha',)
    list_display = ('candidato',
                    'usuario',
                    'sitio_fecha_chile',
                    'sitio_descripcion',
                    )
    exclude = ('sitio',)
    # list_editable = ('sitio_descripcion', )
    readonly_fields = ('sitio_fecha_chile', 'image_tag_img_google_dist_nominal', 'image_tag_img_google_sitio')
    fields = ('candidato',
              'sitio_fecha_chile',
              'sitio_lat',
              'sitio_lon',
              'sitio_descripcion',
              'image_tag_img_google_sitio',
              'image_tag_img_google_dist_nominal')
    ordering = ['sitio_fecha']

    def sitio_fecha_chile(self, obj):
        timezone_chile = pytz.timezone('America/Santiago')
        datetime_chile = obj.sitio_fecha.astimezone(timezone_chile)
        return date_format(datetime_chile, "d/m/Y  -  H:i")
    sitio_fecha_chile.short_description = 'Fecha - Hora'
    sitio_fecha_chile.admin_order_field = 'sitio_fecha'


admin.site.register(RegistroSitio, RegistroSitioAdmin)


# REGISTRO SITIO IMAGENES
class RegistroSitioImagenesInline(admin.StackedInline):
    model = RegistroSitioImagenes
    extra = 0
    # template = 'admin/edit_inline/mosaic.html'
    readonly_fields = ('pic_with_description', 'pic', 'descripcion')
    fieldsets = (
        ('', {
            'fields': (
                'pic_with_description',
            ),
        }),)

    def pic_with_description(self, obj):
        if obj.pic:
            image_html = format_html(
                '<div class="image-with-description"><img src="{}" style="width: 100%; height: auto;"/></div>',
                obj.pic.url)
            description_html = format_html('<div class="inline-description"><p><strong>{}</strong></p></div>',
                                           obj.descripcion if obj.descripcion else "Sin descripción")
            return format_html('{}{}', image_html, description_html)
        return "No hay imagen"

    pic_with_description.short_description = "Imagen y Descripción"


class RegistroSitioImagenesAdmin(admin.ModelAdmin):
    list_display = ('candidato',
                    'image_tag_pic',
                    'descripcion',
                    )
    # exclude = ('sitio',)
    list_editable = ('descripcion',)
    readonly_fields = ('image_tag_pic',)


admin.site.register(RegistroSitioImagenes, RegistroSitioImagenesAdmin)


# REGISTRO ELECTRICO
class RegistroElectricoInline(admin.StackedInline):
    model = RegistioElectrico
    extra = 0
    readonly_fields = ('electrico_no_poste',
                       'electrico_lat', 'electrico_lat_gms',
                       'electrico_lon', 'electrico_lon_gms',
                       'electrico_comentario',
                       'electrico_imagen1_thumbnail',
                       'electrico_imagen2_thumbnail',
                       'img_google_electrico', 'distancia_poste',
                       )
    fieldsets = (
        ('', {
            'fields': (
                'electrico_no_poste',
                ('electrico_lat', 'electrico_lat_gms'),
                ('electrico_lon', 'electrico_lon_gms'),
                ('electrico_imagen1_thumbnail', 'electrico_comentario'),
                ('electrico_imagen2_thumbnail',),
                ('img_google_electrico', 'distancia_poste'),
                # ('electrico_google_thumbnail', 'distancia_coordenadas'),

            ),
        }),)

    def electrico_imagen1_thumbnail(self, obj):
        if obj.electrico_imagen1:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.electrico_imagen1.url)
        return "No hay imagen"

    electrico_imagen1_thumbnail.short_description = 'Imagen Poste'

    def electrico_imagen2_thumbnail(self, obj):
        if obj.electrico_imagen2:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.electrico_imagen2.url)
        return "No hay imagen"

    electrico_imagen2_thumbnail.short_description = 'Imagen Electrico'

    def electrico_lat_gms(self, obj):
        return dec_to_gms(obj.electrico_lat)

    electrico_lat_gms.short_description = "Latitud (GMS)"

    def electrico_lon_gms(self, obj):
        return dec_to_gms(obj.electrico_lon)

    electrico_lon_gms.short_description = "Longitud (GMS)"

    def img_google_electrico(self, obj):
        if obj.electrico_img_google:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="480" height=""/>', obj.electrico_img_google.url)
        return "No hay imagen"

    img_google_electrico.short_description = 'Imagen Satelital Sitio & Empalme Electrico'

    def distancia_poste(self, obj):
        try:
            # Acceder a RegistroSitio a través de la relación Candidato
            registro_sitio = obj.candidato.registrositio
            if obj.electrico_lat and registro_sitio.sitio_lat:
                distancia = calcular_distancia_geopy(
                    obj.electrico_lat,
                    obj.electrico_lon,
                    registro_sitio.sitio_lat,
                    registro_sitio.sitio_lon
                )
                return f"{round(distancia, 2)} m"
        except AttributeError:
            return "Sin coordenadas"
        except Exception as e:
            # Manejo de cualquier otro error no esperado
            print(f"Error al calcular la distancia: {e}")
            return "Error en cálculo"
        return "Sin distancia"

    distancia_poste.short_description = 'Distancia a Empalme electrico'


class RegistioElectricoAdmin(admin.ModelAdmin):
    list_display = ('candidato',
                    'usuario',
                    'electrico_no_poste',
                    'electrico_comentario',
                    )
    exclude = ('sitio',)

admin.site.register(RegistioElectrico, RegistioElectricoAdmin)


# REGISTRO CAMPO
class CandidatoAdmin(admin.ModelAdmin):
    user_model = None
    list_display = ('candidato', 'sitio_nombre', 'usuario_nombre', 'sitio_empresa',  'formatted_fecha_creacion')

    inlines = [
        RegistroLlegadaInline,
        RegistroLocalidadInline,
        RegistroPropietariodInline,
        RegistroPropiedadInline,
        RegistroSitioInline,
        RegistroSitioImagenesInline,
        RegistroElectricoInline,
    ]

    class Media:
        js = ('js/admin_custom_reg.js',)
        css = {
            'all': ['css/admin_custom_reg.css'],
            }



    # CANDIDATO
    def formatted_fecha_creacion(self, obj):
        timezone_chile = pytz.timezone('America/Santiago')
        datetime_chile = obj.fecha_creacion.astimezone(timezone_chile)
        return date_format(datetime_chile, "d/m/Y  -  H:i")
    formatted_fecha_creacion.short_description = 'Fecha - Hora'
    formatted_fecha_creacion.admin_order_field = 'fecha_creacion'

    def candidato_empresa(self, obj):
        # Asegurarse de que el usuario tiene un UserProfile asociado
        if not hasattr(obj, 'usuario'):
            return "No disponible"
        if hasattr(obj.usuario, 'userprofile'):
            # Asegurarse de que el UserProfile tiene una empresa asociada
            if obj.usuario.userprofile.empresa:
                # Suponiendo que 'Empresa' tiene un campo llamado 'pais' para el país
                empresa_nombre = obj.usuario.userprofile.empresa.nombre
                empresa_pais = obj.usuario.userprofile.empresa.pais
                return f"{empresa_nombre} - {empresa_pais}"
        return "No disponible"
    candidato_empresa.short_description = 'Empresa - País'

    # DATOS PROYECTO
    readonly_fields = (
        'sitio_ID', 'sitio_nombre', 'sitio_altura',
        'sitio_provincia', 'sitio_municipio', 'sitio_localidad',
        'usuario_nombre', 'usuario_user', 'usuario_telf', 'sitio_empresa',
        'sitio_lat_nominal', 'sitio_lat_nominal_gms',
        'sitio_lon_nominal', 'sitio_lon_nominal_gms',
        'imagen_gmaps'
    )

    fieldsets = (
        ('Datos de Proyecto', {
            'fields': (
                ('sitio_ID', 'sitio_nombre', 'sitio_altura'),
                ('sitio_provincia', 'sitio_municipio', 'sitio_localidad',),
                ('usuario_nombre', 'usuario_user', 'usuario_telf', 'sitio_empresa'),
                ('sitio_lat_nominal', 'sitio_lat_nominal_gms'),
                ('sitio_lon_nominal', 'sitio_lon_nominal_gms'),
                'imagen_gmaps',
            ),
            # 'classes': ('collapse',),  # Hace este grupo colapsable
            # 'description': ('Esta sección contiene <b>información detallada</b> sobre el sitio del proyecto.'
            #                 ' Para más detalles, <a href="https://example.com">visita este enlace</a>.')
        }),
    )

    def get_llegada(self, obj):
        llegada = RegistroLlegada.objects.filter(candidato=obj).annotate(
            usuario_telf=F('usuario__userprofile__telf'),
            user_profile=F('usuario__userprofile'),
        ).first()

        if llegada:
            llegada.user_profile = UserProfile.objects.filter(user=llegada.usuario).first()
            return llegada

        return None

    def sitio_ID(self, obj):
        return f"{obj.sitio.PTICellID}"
    sitio_ID.short_description = 'PTI ID'

    def sitio_nombre(self, obj):
        return f"{obj.sitio.nombre}"
    sitio_nombre.short_description = 'Nombre'

    def sitio_lat_nominal(self, obj):
        return f"{obj.sitio.lat_nominal}"

    sitio_lat_nominal.short_description = 'Latitud Nominal'

    def sitio_lat_nominal_gms(self, obj):
        return dec_to_gms(obj.sitio.lat_nominal)

    sitio_lat_nominal_gms.short_description = "Latitud Nominal (GMS)"

    def sitio_lon_nominal(self, obj):
        return f"{obj.sitio.lon_nominal}"

    sitio_lon_nominal.short_description = 'Longitud Nominal'

    def sitio_lon_nominal_gms(self, obj):
        return dec_to_gms(obj.sitio.lon_nominal)

    sitio_lon_nominal_gms.short_description = "Longitud Nominal (GMS)"

    def sitio_altura(self, obj):
        return f"{obj.sitio.altura} m."

    sitio_altura.short_description = 'Altura'

    def sitio_provincia(self, obj):
        return f"{obj.sitio.provincia}"

    sitio_provincia.short_description = 'Provincia'

    def sitio_municipio(self, obj):
        return f"{obj.sitio.municipio}"

    sitio_municipio.short_description = 'Municipio'

    def sitio_localidad(self, obj):
        return f"{obj.sitio.localidad}"

    sitio_localidad.short_description = 'Localidad'

    def sitio_empresa(self, obj):
        return f"{obj.sitio.empresa}"

    sitio_empresa.short_description = 'Empresa'

    def usuario_nombre(self, obj):
        return self.get_llegada(obj).user_profile.get_full_name if self.get_llegada(obj) else "Sin nombre"

    usuario_nombre.short_description = 'Buscador'

    def usuario_user(self, obj):
        return self.get_llegada(obj).usuario.username if self.get_llegada(obj) else "Sin nombre"

    usuario_user.short_description = 'Username'

    def usuario_telf(self, obj):
        return self.get_llegada(obj).usuario_telf if self.get_llegada(obj) else "Sin teléfono"

    usuario_telf.short_description = 'Teléfono'

    def imagen_gmaps(self, obj):
        if obj.sitio.img_google:
            return format_html('<img src="{}" width="480" height=""/>', obj.sitio.img_google.url)
        return "Sin imagen"

    imagen_gmaps.short_description = 'Imagen Satelital (coordenadas nominales)'


admin.site.register(Candidato, CandidatoAdmin)

