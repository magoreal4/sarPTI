from django.contrib import admin
from django.utils.html import format_html
from .models import (Servicio, 
                     Usuario, 
                     Sitio, 
                     RegistroLlegada, 
                     RegistroLocalidad,
                     RegistroPropietario,
                     RegistroPropiedad,
                     RegistroSitio,
                     RegistroSitioImagenes,
                     RegistioElectrico
                     )
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'pais', 'empresa')
admin.site.register(Servicio, ServicioAdmin)

class SitioAdmin(admin.ModelAdmin):
    list_display = ('pais_empresa', 'PTICellID', 'nombre')  
admin.site.register(Sitio, SitioAdmin)

class   UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'telf', 'pais_empresa')  
    list_editable = ('telf', 'pais_empresa')
admin.site.register(Usuario, UsuarioAdmin)

# admin.site.register(RegistroLlegada)

# admin.site.register(RegistroLocalidad)

# admin.site.register(RegistroPropietario)

# admin.site.register(RegistroPropiedad)

# admin.site.register(RegistroSitio)

# admin.site.register(RegistroSitioImagenes)

# admin.site.register(RegistioElectrico)


# Clases Inline para cada modelo relacionado
class RegistroLocalidadInline(admin.StackedInline):
    model = RegistroLocalidad
    extra = 0
    fields = ('municipio', 'localidad', 'energia_localidad')
    readonly_fields = ( 'municipio', 'localidad', 'energia_localidad',)



class RegistroPropietarioInline(admin.StackedInline):
    model = RegistroPropietario
    extra = 0
    fields =('propietario_born',
            'propietario_ci',
            'propietario_telf',
            'propietario_direccion',
            'propietario_estado_civil',)

    readonly_fields =('propietario_born',
            'propietario_ci',
            'propietario_telf',
            'propietario_direccion',
            'propietario_estado_civil',)


class RegistroPropiedadInline(admin.StackedInline):
    model = RegistroPropiedad
    extra = 0
    fields =('propiedad_escritura',
            'propiedad_registro_civil',
            'propiedad_imagen_thumbnail',
            'propiedad_imagen',
            'propiedad_descripcion',)
    readonly_fields =('propiedad_escritura',
            'propiedad_registro_civil',
            'propiedad_imagen_thumbnail',
            'propiedad_descripcion',)
    
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
    readonly_fields =('sitio_fecha',
            'sitio_lat',
            'sitio_lon',
            'sitio_imagen_thumbnail',
            'sitio_descripcion',)

    def sitio_imagen_thumbnail(self, obj):
        if obj.sitio_imagen:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.sitio_imagen.url)
        return "No hay imagen"
    sitio_imagen_thumbnail.short_description = 'Imagen Principal de la Propiedad'

class RegistroSitioImagenesInline(admin.StackedInline):
    model = RegistroSitioImagenes
    extra = 0
    fields =('pic_with_description', 'pic')
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
    readonly_fields =('electrico_no_poste',
            'electrico_lat',
            'electrico_lon',
            'electrico_comentario',
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
class RegistroLlegadaAdmin(admin.ModelAdmin):
    inlines = [
        RegistroLocalidadInline,
        RegistroPropietarioInline,
        RegistroPropiedadInline,
        RegistroSitioInline,
        RegistroSitioImagenesInline,
        RegistioElectricoInline,
    ]
    readonly_fields = (
        'sitio', 
        'sitio_nombre', 
        'sitio_altura',
        'pais_empresa', 
        'candidato', 
        'usuario',
        'sitio_latitud',
        'sitio_longitud',
        'status_llegada',
        'sitio_imagen',
        'observaciones',
        )
    list_display = (
        'sitio', 
        'sitio_nombre', 
        'sitio_altura',
        'pais_empresa', 
        )
    fieldsets = (
        ('Información General', {  # Ajusta los títulos y campos según necesites
            'fields': (
                'pais_empresa',
                ('sitio', 'sitio_nombre', 'sitio_altura'),
                ('usuario', 'candidato'),
                ('sitio_latitud', 'sitio_longitud'),
                ),
        }),
        ('Información de Llegada', {
            'fields': (
                'status_llegada',
                ('sitio_imagen', 'observaciones'),
                'imagen_llegada',
                ),
        })
        )
    def pais_empresa(self, obj):
        # Intenta recuperar el objeto Usuario relacionado al user de RegistroLlegada
        try:
            usuario = Usuario.objects.get(user=obj.usuario)
            return usuario.pais_empresa
        except Usuario.DoesNotExist:
            return "No definido"  # O puedes retornar un valor que indique que no se encontró el Usuario
    pais_empresa.short_description = 'País Empresa' 
    
    def sitio_nombre(self, obj):
        return obj.sitio.nombre
    sitio_nombre.short_description = 'Nombre'
    
    def sitio_altura(self, obj):
        return f"{obj.sitio.altura} m."
    sitio_altura.short_description = 'Altura'
    
    def sitio_latitud(self, obj):
        return f"{obj.sitio.lat_nominal}"
    sitio_latitud.short_description = 'Latitud'
    
    def sitio_longitud(self, obj):
        return f"{obj.sitio.lon_nominal}"
    sitio_longitud.short_description = 'Longitud'
    
    def sitio_imagen(self, obj):
        if obj.imagen_llegada:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="320" height=""/>', obj.imagen_llegada.url)
        return "No hay imagen"
    sitio_imagen.short_description = 'Imagen llegada localidad'
        
admin.site.register(RegistroLlegada, RegistroLlegadaAdmin)