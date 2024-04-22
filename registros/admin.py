from django.contrib import admin
from django.utils.html import format_html
from django.utils.formats import date_format
from geopy.distance import geodesic
from .models import (Empresa, 
                     Usuario, 
                     Sitio, 
                     Candidato, 
                     RegistroLlegada, 
                     RegistroLocalidad,
                     RegistroPropietario,
                     RegistroPropiedad,
                     RegistroSitio,
                     RegistroSitioImagenes,
                     RegistioElectrico
                     )
from semantic_admin import SemanticModelAdmin, SemanticStackedInline, SemanticTabularInline
from semantic_admin.contrib.import_export.admin import SemanticImportExportModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

def dec_to_gms(decimal_deg, is_lat=True):
    if decimal_deg is None or decimal_deg == "":
        return "-"
    # Determina si el grado es negativo (Sur o Oeste)
    is_negative = decimal_deg < 0
    # Convierte el grado a positivo para el cálculo
    decimal_deg = abs(decimal_deg)
    
    degrees = int(decimal_deg)
    minutes = int((decimal_deg - degrees) * 60)
    seconds = (decimal_deg - degrees - minutes/60) * 3600.00

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
    list_display = ('id', 'pais', 'nombre')
admin.site.register(Empresa, EmpresaAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nombre', 'telf', 'empresa')  
    list_editable = ('empresa', )
admin.site.register(Usuario, UsuarioAdmin)


class SitiosResource(resources.ModelResource):
    class Meta:
        model = Sitio

# class SitioAdmin(admin.ModelAdmin):
#     list_display = ('PTICellID', 'nombre', 'altura', 'empresa','id' )  
#     list_editable = ('empresa', )


class SitioAdmin(SemanticImportExportModelAdmin):
    resource_class = SitiosResource
    list_display = ('PTICellID', 'nombre', 'altura', 'empresa', 'id')
    list_editable = ('empresa', )
admin.site.register(Sitio, SitioAdmin)
        
# class SitioImportExportAdmin(SemanticImportExportModelAdmin):
#     resource_class = SitiosResource
#     list_display = (
#         'PTICellID',
#         'EntelID',
#         'nombre_modificado',
#         'altura',
#         'lat_nombre',
#         'lon_nombre',
#     )

    # class Meta:
    #     model = Sitio



# class RegistroSitioAdmin(admin.ModelAdmin):
#     list_display = ('sitio_lat', 'sitio_lon',  )
# admin.site.register(RegistroSitio, RegistroSitioAdmin)


# admin.site.register(RegistroLocalidad)

# admin.site.register(RegistroPropietario)

# admin.site.register(RegistroPropiedad)

# admin.site.register(RegistroSitioImagenes)

# admin.site.register(RegistioElectrico)

# admin.site.register(Candidato)



class RegistroLlegadaInline(SemanticStackedInline):
    model = RegistroLlegada
    extra = 0
    readonly_fields = (
        'fecha_llegada', 'status_llegada',
        'lat_llegada', 'lat_llegada_gms',
        'lon_llegada', 'lon_llegada_gms',
        'imagen_llegada_preview', 'observaciones',
        )
    fieldsets = (
    ('', {  
        'fields': (    
            ('fecha_llegada', 'status_llegada',),  
            ('lat_llegada', 'lat_llegada_gms',  ),
            ('lon_llegada', 'lon_llegada_gms', ),
            ('imagen_llegada_preview', 'observaciones'),

        ),
    }),)	
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
    imagen_llegada_preview.short_description = 'Vista Previa de la Imagen'
    
# Clases Inline para cada modelo relacionado
class RegistroLocalidadInline(SemanticStackedInline):
    model = RegistroLocalidad
    extra = 0
    readonly_fields = ('provincia','municipio', 'localidad', 'energia_localidad_mensaje')
    fieldsets = (
                ('', {  
                    'fields': (    
                        ('provincia', 'municipio','localidad'),
                        ('energia_localidad_mensaje')
                    ),
                }),)	
    def energia_localidad_mensaje(self, obj):
        if obj.energia_localidad:
            return "Cuenta con energía Electríca"
        else:
            return "No Cuenta con energía Electríca"
    energia_localidad_mensaje.short_description = "Energía Ecéctrica"

class RegistroPropietarioInline(SemanticStackedInline):
    model = RegistroPropietario
    extra = 0
    readonly_fields =('propietario_nombre_apellido',
             'fecha_nacimiento',
             'propietario_ci',
             'propietario_telf',
             'propietario_direccion',
             'propietario_estado_civil_mensaje',)
    fieldsets = (
            ('', {  
                'fields': (
                    'propietario_nombre_apellido',
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
    
class RegistroPropiedadInline(SemanticStackedInline):
    model = RegistroPropiedad
    extra = 0
    readonly_fields =('propiedad_rol','propiedad_escritura',
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

class RegistroSitioInline(SemanticStackedInline):
    model = RegistroSitio
    extra = 0
    readonly_fields =('sitio_fecha',
            'sitio_lat', 'sitio_lat_gms',
            'sitio_lon', 'sitio_lon_gms',
            'sitio_imagen_thumbnail',
            'sitio_imagen',
            'sitio_descripcion',
            'sitio_google_thumbnail',
            'distancia_coordenadas')
    fieldsets = (
            ('', {  
                'fields': (
                    'sitio_fecha', 
                    ('sitio_lat', 'sitio_lat_gms'),
                    ('sitio_lon', 'sitio_lon_gms'),
                    ('sitio_imagen_thumbnail', 'sitio_descripcion'),
                    ('sitio_google_thumbnail', 'distancia_coordenadas',),
                    
                ),
            }),)
    
    def sitio_imagen_thumbnail(self, obj):
        if obj.sitio_imagen:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.sitio_imagen.url)
        return "No hay imagen"
    sitio_imagen_thumbnail.short_description = 'Imagen Principal de Sitio'
    
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
        
    def sitio_google_thumbnail(self, obj):
        if obj.sitio_img_google:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.sitio_img_google.url)
        return "No hay imagen"
    sitio_google_thumbnail.short_description = 'Imagen Google'

    def sitio_lat_gms(self, obj):
        return dec_to_gms(obj.sitio_lat)
    sitio_lat_gms.short_description = "Latitud Torre (GMS)"
    
    def sitio_lon_gms(self, obj):
        return dec_to_gms(obj.sitio_lon)
    sitio_lon_gms.short_description = "Longitud Torre (GMS)"
    

class RegistroSitioImagenesInline(SemanticStackedInline):
    model = RegistroSitioImagenes
    extra = 0
    fields =('pic_with_description', 'pic', 'descripcion')
    readonly_fields =('pic_with_description',)
    
    def pic_with_description(self, obj):
        # Verificar si hay una imagen y una descripción disponibles
        if obj.pic:
            image_html = format_html('<img src="{}" width="320" height="auto"/>', obj.pic.url)
            description_html = format_html('<p style="margin-top: 10px;"><strong> {}</p>', obj.descripcion if obj.descripcion else "Sin descripción" '</strong>')
            return image_html + description_html
        return "No hay imagen"
    
    pic_with_description.short_description = "Imagen y Descripción"

    
class RegistioElectricoInline(SemanticStackedInline):
    model = RegistioElectrico
    extra = 0
    # fields =('electrico_no_poste',
    #         'electrico_lat',
    #         'electrico_lon',
    #         'electrico_comentario',
    #         'electrico_imagen1_thumbnail',
    #         'electrico_imagen1',
    #         'electrico_imagen2_thumbnail',
    #         'electrico_imagen2',)
    readonly_fields =('electrico_no_poste',
            'electrico_lat', 'electrico_lat_gms',
            'electrico_lon','electrico_lon_gms',
            'electrico_comentario',
            'electrico_imagen1_thumbnail',
            'electrico_imagen2_thumbnail',
            # 'electrico_google_thumbnail', 'distancia_coordenadas'
            )
    fieldsets = (
        ('', {  
            'fields': (
                'electrico_no_poste', 
                ('electrico_lat', 'electrico_lat_gms'),
                ('electrico_lon', 'electrico_lon_gms'),
                ('electrico_imagen1_thumbnail', 'electrico_comentario'),
                'electrico_imagen2_thumbnail',
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
    electrico_imagen2_thumbnail.short_description = 'Imagen Sistema electrico'
    
    # def distancia_coordenadas(self, obj):
    #     sitio_relacionado = RegistroSitio.objects.filter(candidato=obj.campo_comun).first()
    #     if sitio_relacionado and obj.electrico_lat:
    #         distancia = calcular_distancia_geopy(
    #             obj.electrico_lat, 
    #             obj.electrico_lon, 
    #             sitio_relacionado.sitio_lat, 
    #             sitio_relacionado.sitio_lon
    #         )
    #         return f"{round(distancia, 2)} m" 
    #     return "Sin distancia"
    # distancia_coordenadas.short_description = 'Distancia a Coordenadas nominales'
        
    # def electrico_google_thumbnail(self, obj):
    #     if obj.electrico_img_google:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
    #         return format_html('<img src="{}" width="320" height=""/>', obj.electrico_img_google.url)
    #     return "No hay imagen"
    # electrico_google_thumbnail.short_description = 'Imagen Google'

    def electrico_lat_gms(self, obj):
        return dec_to_gms(obj.electrico_lat)
    electrico_lat_gms.short_description = "Latitud (GMS)"
    
    def electrico_lon_gms(self, obj):
        return dec_to_gms(obj.electrico_lon)
    electrico_lon_gms.short_description = "Longitud (GMS)"


class CandidatoAdmin(SemanticModelAdmin):
    inlines = [
        RegistroLlegadaInline,
        RegistroLocalidadInline,
        RegistroPropietarioInline,
        RegistroPropiedadInline,
        RegistroSitioInline,
        # RegistroSitioImagenesInline,
        RegistioElectricoInline,
    ]
    list_display = (
        # 'id', 
        'sitio', 
        'sitio_nombre',
        'sitio_altura',
        'candidato', 
        'formatted_fecha_creacion'
        )
    readonly_fields = ('id',
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
                ('sitio_ID', 'sitio_nombre', 'sitio_altura' ),
                ('sitio_provincia', 'sitio_municipio', 'sitio_localidad', ),
                ('usuario_nombre', 'usuario_user', 'usuario_telf', 'sitio_empresa'),
                ('sitio_lat_nominal', 'sitio_lat_nominal_gms' ),
                ('sitio_lon_nominal', 'sitio_lon_nominal_gms' ),
                'imagen_gmaps',
                ),

            # 'description': 'Esta sección contiene <b>información detallada</b> sobre el sitio del proyecto. Para más detalles, <a href="https://example.com">visita este enlace</a>.'
    
        }),
    )
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
        return f"{obj.usuario.nombre}"
    usuario_nombre.short_description = 'Buscador'

    def usuario_user(self, obj):
        return f"{obj.usuario.user}"
    usuario_user.short_description = 'Username'

    def usuario_telf(self, obj):
        return f"{obj.usuario.telf}"
    usuario_telf.short_description = 'Telefono'    
    
    def formatted_fecha_creacion(self, obj):
        return date_format(obj.fecha_creacion, "d/m/Y H:i")
    formatted_fecha_creacion.short_description = 'Fecha'
    formatted_fecha_creacion.admin_order_field = 'fecha_creacion'  # Permite ordenar por este campo en el admin
    
    def imagen_gmaps(self, obj):
        if obj.sitio.img_google:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="480" height=""/>', obj.sitio.img_google.url)
        return "No hay imagen"
    imagen_gmaps.short_description = 'Vista Previa de la Imagen'
    
    


admin.site.register(Candidato, CandidatoAdmin)
