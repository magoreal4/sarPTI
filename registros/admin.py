from django.contrib import admin
from django.utils.html import format_html
from django.utils.formats import date_format
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

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pais', 'nombre')

# class SitioAdmin(admin.ModelAdmin):
    # list_display = ('PTICellID', 'nombre', 'empresa', 'altura' )
    # list_editable = ('empresa',)  
admin.site.register(Sitio)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nombre', 'telf', 'empresa')  
    list_editable = ('empresa', )
admin.site.register(Usuario, UsuarioAdmin)

admin.site.register(Empresa, EmpresaAdmin)

# admin.site.register(RegistroLocalidad)

# admin.site.register(RegistroPropietario)

# admin.site.register(RegistroPropiedad)

# admin.site.register(RegistroSitio)

# admin.site.register(RegistroSitioImagenes)

# admin.site.register(RegistioElectrico)

# admin.site.register(Candidato)



class RegistroLlegadaInline(admin.StackedInline):
    model = RegistroLlegada
    extra = 0  # Número de formas extra vacías que se mostrarán
# admin.site.register(RegistroLlegada)

# Clases Inline para cada modelo relacionado
class RegistroLocalidadInline(admin.StackedInline):
    model = RegistroLocalidad
    extra = 0
    fields = ('municipio', 'localidad', 'energia_localidad')
    # readonly_fields = ( 'municipio', 'localidad', 'energia_localidad',)



class RegistroPropietarioInline(admin.StackedInline):
    model = RegistroPropietario
    extra = 0
    fields =('propietario_nombre_apellido',
             'propietario_born',
             'propietario_ci',
             'propietario_telf',
             'propietario_direccion',
             'propietario_estado_civil',)

    # readonly_fields =('propietario_born',
    #         'propietario_ci',
    #         'propietario_telf',
    #         'propietario_direccion',
    #         'propietario_estado_civil',)


class RegistroPropiedadInline(admin.StackedInline):
    model = RegistroPropiedad
    extra = 0
    fields =('propiedad_escritura',
            'propiedad_registro_civil',
            'propiedad_imagen_thumbnail',
            'propiedad_imagen',
            'propiedad_descripcion',)
    # readonly_fields =('propiedad_escritura',
    #         'propiedad_registro_civil',
    #         'propiedad_imagen_thumbnail',
    #         'propiedad_descripcion',)
    readonly_fields =('propiedad_imagen_thumbnail',)
    
    def propiedad_imagen_thumbnail(self, obj):
        if obj.propiedad_imagen:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.propiedad_imagen.url)
        return "No hay imagen"
    propiedad_imagen_thumbnail.short_description = 'Imagen Principal de la Propiedad'

class RegistroSitioInline(admin.StackedInline):
    model = RegistroSitio
    extra = 0
    fields =('sitio_fecha',
            'sitio_lat',
            'sitio_lon',
            'sitio_imagen_thumbnail',
            'sitio_imagen',
            'sitio_descripcion',)
    # readonly_fields =('sitio_fecha',
    #         'sitio_lat',
    #         'sitio_lon',
    #         'sitio_imagen_thumbnail',
    #         'sitio_descripcion',)
    readonly_fields =('sitio_imagen_thumbnail',)
    def sitio_imagen_thumbnail(self, obj):
        if obj.sitio_imagen:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.sitio_imagen.url)
        return "No hay imagen"
    sitio_imagen_thumbnail.short_description = 'Imagen Principal de Sitio'

class RegistroSitioImagenesInline(admin.StackedInline):
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

    
class RegistioElectricoInline(admin.StackedInline):
    model = RegistioElectrico
    extra = 0
    fields =('electrico_no_poste',
            'electrico_lat',
            'electrico_lon',
            'electrico_comentario',
            'electrico_imagen1_thumbnail',
            'electrico_imagen1',
            'electrico_imagen2_thumbnail',
            'electrico_imagen2',)
    # readonly_fields =('electrico_no_poste',
    #         'electrico_lat',
    #         'electrico_lon',
    #         'electrico_comentario',
    #         'electrico_imagen1_thumbnail',
    #         'electrico_imagen2_thumbnail',)
    readonly_fields =(
            'electrico_imagen1_thumbnail',
            'electrico_imagen2_thumbnail',)
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
    
# Admin para RegistroLlegada
# class RegistroLlegadaAdmin(admin.ModelAdmin):
#     inlines = [
#         RegistroLocalidadInline,
#         RegistroPropietarioInline,
#         RegistroPropiedadInline,
#         RegistroSitioInline,
#         RegistroSitioImagenesInline,
#         RegistioElectricoInline,
#     ]
    # readonly_fields = (
    #     'sitio', 
    #     'sitio_nombre', 
    #     'sitio_altura',
    #     'sitio_empresa', 
    #     'candidato', 
    #     'usuario',
    #     'sitio_latitud',
    #     'sitio_longitud',
    #     'status_llegada',
    #     'sitio_imagen',
    #     'observaciones',
    #     )
    # list_display = (
    #     'sitio', 
    #     'sitio_nombre', 
    #     'sitio_altura',
    #     'sitio_empresa', 
    #     'candidato', 
    #     'usuario',
    #     'lat_llegada',
    #     'lon_llegada',
    #     'status_llegada',
    #     'sitio_imagen',
    #     'observaciones',
    #     )
    # fieldsets = (
    #     ('Información General', {  # Ajusta los títulos y campos según necesites
    #         'fields': (
    #             'sitio_empresa',
    #             ('sitio', 'sitio_nombre', 'sitio_altura'),
    #             ('usuario', 'candidato'),
    #             ('sitio_latitud', 'sitio_longitud'),
    #             ),
    #     }),
    #     ('Información de Llegada', {
    #         'fields': (
    #             'status_llegada',
    #             ('sitio_imagen', 'observaciones'),
    #             'imagen_llegada',
    #             ),
    #     })
    #     )
#     def sitio_empresa(self, obj):
#         # Intenta recuperar el objeto Usuario relacionado al user de RegistroLlegada
#         try:
#             usuario = Usuario.objects.get(user=obj.usuario)
#             return usuario.empresa
#         except Usuario.DoesNotExist:
#             return "No definido"  # O puedes retornar un valor que indique que no se encontró el Usuario
#     sitio_empresa.short_description = 'País Empresa' 
    
#     def sitio_nombre(self, obj):
#         return obj.sitio.nombre
#     sitio_nombre.short_description = 'Nombre'
    
#     def sitio_altura(self, obj):
#         return f"{obj.sitio.altura} m."
#     sitio_altura.short_description = 'Altura'
    
#     def sitio_latitud(self, obj):
#         return f"{obj.sitio.lat_nominal}"
#     sitio_latitud.short_description = 'Latitud'
    
#     def sitio_longitud(self, obj):
#         return f"{obj.sitio.lon_nominal}"
#     sitio_longitud.short_description = 'Longitud'
    
#     def sitio_imagen(self, obj):
#         if obj.imagen_llegada:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
#             return format_html('<img src="{}" width="320" height=""/>', obj.imagen_llegada.url)
#         return "No hay imagen"
#     sitio_imagen.short_description = 'Imagen llegada localidad'
        
# admin.site.register(RegistroLlegada, RegistroLlegadaAdmin)

class CandidatoAdmin(admin.ModelAdmin):
    inlines = [
        RegistroLlegadaInline,
        RegistroLocalidadInline,
        RegistroPropietarioInline,
        RegistroPropiedadInline,
        RegistroSitioInline,
        RegistroSitioImagenesInline,
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
            return format_html('<img src="{}" width="620" height=""/>', obj.sitio.img_google.url)
        return "No hay imagen"
    imagen_gmaps.short_description = 'Vista Previa de la Imagen'
    
    
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
    # fieldsets = (
    #     ('Información General', {  # Ajusta los títulos y campos según necesites
    #         'fields': (
    #             'sitio_empresa',
    #             ('sitio', 'sitio_nombre', 'sitio_altura'),
    #             ('usuario', 'candidato'),
    #             ('sitio_latitud', 'sitio_longitud'),
    #             ),
    #     }),
    #     ('Información de Llegada', {
    #         'fields': (
    #             'status_llegada',
    #             ('sitio_imagen', 'observaciones'),
    #             'imagen_llegada',
    #             ),
    #     })
    #     )

admin.site.register(Candidato, CandidatoAdmin)
