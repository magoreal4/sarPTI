from django.contrib import admin
from .models import RegistroInicio
from .forms import RegistroInicioForm
from django.utils.html import format_html
from .models import (
    RegistroInicio,
    Imagenes,
    InformacionGeneral,
    InformacionPropiedad,
    Croquis,
    InfTecPropiedad,
    Documentos,
    )




class ImagenesAdmin(admin.ModelAdmin):
    list_display = ('registro_inicio',
                    'image_tag_pic',
                    'descripcion',
                    )
    exclude = ('sitio',)
    list_editable = ('descripcion',)
    readonly_fields = ('image_tag_pic',)

admin.site.register(Imagenes, ImagenesAdmin)

class ImagenesInline(admin.StackedInline):
    model = Imagenes
    extra = 0
    readonly_fields = ('pic_with_description',)
    fieldsets = (
        ('', {
            'fields': (
                'pic_with_description',
                'imagen',
                'descripcion',
            ),
        }),)

    def pic_with_description(self, obj):
        if obj.imagen:
            image_html = format_html(
                '<div class="image-with-description"><img src="{}" style="width: 100%; height: auto;"/></div>',
                obj.imagen.url)
            description_html = format_html('<div class="inline-description"><p><strong>{}</strong></p></div>',
                                           obj.descripcion if obj.descripcion else "Sin descripción")
            return format_html('{}{}', image_html, description_html)
        return "No hay imagen"
    pic_with_description.short_description = "Imagen y Descripción"


    


class InformacionGeneralInline(admin.StackedInline):
    model = InformacionGeneral
    extra = 0
    # readonly_fields = ('fecha_visita', 'propietario', 'propietario_telf', 'propietario_direccion', 'propietario_email', 'estado_civil')
    fieldsets = (
        ('', {
            'fields': (
                ('propietario', 'propietario_telf',),
                ( 'propietario_email', 'propietario_direccion', ),
                'estado_civil',
            ),
 
        }),
    )
    class Media:
        js = ('js/propietario.js',)

    

class InformacionGeneralAdmin(admin.ModelAdmin):
    list_display = ['registro_inicio', 'propietario', 'propietario_telf', 'propietario_email']
    list_editable = ('propietario_telf', 'propietario_email')
admin.site.register(InformacionGeneral, InformacionGeneralAdmin)


class InformacionPropiedadAdmin(admin.ModelAdmin):
    list_display = ['registro_inicio', 'propiedad_hipoteca', 'estado_impuestos', 'tiempo_negociado']
admin.site.register(InformacionPropiedad, InformacionPropiedadAdmin)

class InformacionPropiedadInline(admin.StackedInline):
    model = InformacionPropiedad
    extra = 0
    # readonly_fields = ('fecha_visita', 'propietario', 'propietario_telf', 'propietario_direccion', 'propietario_email', 'estado_civil')
    fieldsets = (
        ('', {
            'fields': (
                ('propiedad_hipoteca', 'estado_impuestos'),
                 'tiempo_negociado',
                ('apreciaciones','comentarios'),
            ),
        }),
    )
    

class CroquisAdmin(admin.ModelAdmin):
    list_display = ('registro_inicio',
                'image_tag_pic',
                'descripcion',
                )
    
admin.site.register(Croquis, CroquisAdmin)

class CroquisInline(admin.StackedInline):
    model = Croquis
    extra = 0
    readonly_fields = ('image_tag_pic',)
    fieldsets = (
        ('', {
            'fields': (
                'image_tag_pic',
                ('croquis', 'descripcion'),
            ),
            # 'classes': ('collapse',),  # Hace este grupo colapsable
            'description': ('Croquis del sitio respecto a la propiedad y acceso')
        }),
    )
    
    def imagen_croquis(self, obj):
        if obj.croquis:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
            return format_html('<img src="{}" width="480" height=""/>', obj.croquis.url)
        return "No hay imagen"
    imagen_croquis.short_description = 'Croquis'
    

class InfTecPropiedadAdmin(admin.ModelAdmin):
    list_display = ['registro_inicio', 'dim_frente', 'dim_largo']
admin.site.register(InfTecPropiedad,InfTecPropiedadAdmin)

class InfTecPropiedadInline(admin.StackedInline):
    model = InfTecPropiedad
    extra = 0
    # readonly_fields = ('fecha_visita', 'propietario', 'propietario_telf', 'propietario_direccion', 'propietario_email', 'estado_civil')
    fieldsets = (
        ('Dimensiones', {
            'fields': (
                ('dim_frente', 'dim_largo', 'area'),
                'dim_ampliar'
            ),        
            # 'classes': ('collapse',),  # Hace este grupo colapsable
            # 'description': ('Esta sección contiene <b>información detallada</b> sobre el sitio del proyecto.'
            #                 ' Para más detalles, <a href="https://example.com">visita este enlace</a>.')
        }),
        ('Terreno', {
            'fields': (
                ('forma_terreno', 'topografia_terreno', 'uso_terreno'),
                ('material_terreno', 'desc_acceso_sitio'),
            ),
        
        }),
        ('Acceso al Sitio', {
            'fields': (
                ('dim_acceso', 'condiciones_acceso'),
                ('tipo_carretera', 'acceso_sitio'),
                'cond_acceso_equipo',
            ),
        }),
        ('Entorno', {
            'fields': (
                ('desc_const_aledanas', 'desc_const_importantes'),
                ('riesgo_inundaciones', 'consideraciones_ambientales'),
            ),
        }),
        ('Adicionales', {
            'fields': (
                'obras_civiles_especiales',
                ('demoliciones', 'mov_tierras', 'muros_contencion'),
                ('tala_arboles', 'cons_camino'),
                ('const_tendido_electrico', 'colocacion_postes'),
                ('instalacion_transformador', 'canalizacion_subterranea'),
                'comentarios'
            ),
        }),
        ('Servicios', {
            'fields': (
                'proveedor_agua',
                ('proveedor_electrico', 'no_medidor'),
                ('ubicacion_tendido_electrico', 'transformador_capacidad','transformador_distancia'),
            ),
        }),
    )
    

# class DocumentosAdmin(admin.ModelAdmin):
#     list_display = ['registro_inicio', 'imagen_documento', 'descripcion']
#     def imagen_documento(self, obj):
#         if obj.documento:  # Reemplaza 'imagen' con el nombre real de tu campo de imagen en el modelo FormularioPreIng
#             return format_html('<img src="{}" width="120" height=""/>', obj.documento.url)
#         return "No hay imagen"
#     imagen_documento.short_description = 'Croquis'
# admin.site.register(Documentos,DocumentosAdmin)

class DocumentosAdmin(admin.ModelAdmin):
    list_display = ('registro_inicio',
                    'image_tag_pic',
                    'descripcion',
                    )
    exclude = ('sitio',)
    list_editable = ('descripcion',)
    readonly_fields = ('image_tag_pic',)

admin.site.register(Documentos, DocumentosAdmin)




class DocumentosInline(admin.StackedInline):
    model = Documentos
    extra = 0
    # template = 'admin/edit_inline/mosaic.html'
    readonly_fields = ('pic_with_description', )
    fieldsets = (
        ('', {
            'fields': (
                'pic_with_description',
                'documento',
                'descripcion',
            ),
        }),)

    def pic_with_description(self, obj):
        if obj.documento:
            image_html = format_html(
                '<div class="image-with-description"><img src="{}" style="width: 100%; height: auto;"/></div>',
                obj.documento.url)
            description_html = format_html('<div class="inline-description"><p><strong>{}</strong></p></div>',
                                           obj.descripcion if obj.descripcion else "Sin descripción")
            return format_html('{}{}', image_html, description_html)
        return "No hay imagen"
    pic_with_description.short_description = "Imagen y Descripción"



class RegistroInicioAdmin(admin.ModelAdmin):
    form = RegistroInicioForm
    list_display = ('candidato_registro', 'candidato_letra', 'zona', 'ASNM', 'contactos_ingreso', 'ruta_acceso', 'ruta_huella', 'inf_adicional', 'sitio_ID', )
    inlines = [
        ImagenesInline,
        InformacionGeneralInline,
        InformacionPropiedadInline,
        CroquisInline,
        InfTecPropiedadInline,
        DocumentosInline
    ]

    
    def get_form(self, request, obj=None, **kwargs):
        Form = super(RegistroInicioAdmin, self).get_form(request, obj, **kwargs)
        class DynamicForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs.update({'user_id': request.user.id})
                return Form(*args, **kwargs)
        return DynamicForm
    
    class Media:
        js = ('js/admin_custom_reggab.js',)
        css = {
            'all': ['css/admin_custom_reggab.css'],
            }

        
    list_display = ('candidato_registro', 'candidato_letra', 'zona', 'ASNM', )
    
    readonly_fields = ('sitio_ID', )
    fieldsets = (
        ('Datos Generales', {
            'fields': (
                ('sitio_ID', 'candidato_registro', ),
                ('candidato_letra', 'radio_busqueda', ),
                ('tipo_solucion', 'zona', 'ASNM', ),
                ('contactos_ingreso', 'ruta_acceso' ),
                ('ruta_huella', 'inf_adicional' ),

            ),
            # 'classes': ('collapse',),  # Hace este grupo colapsable
            # 'description': ('Esta sección contiene <b>información detallada</b> sobre el sitio del proyecto.'
            #                 ' Para más detalles, <a href="https://example.com">visita este enlace</a>.')
        }),
    )

    def sitio_ID(self, obj):
        texto = str(obj.candidato_registro)
        return texto[:-2]
    sitio_ID.short_description = 'PTI ID'
    
    
admin.site.register(RegistroInicio, RegistroInicioAdmin)