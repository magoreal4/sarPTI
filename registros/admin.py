from django.contrib import admin

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
    list_display = ('pais_empresa', 'PTICellID', 'nombre')  # Reemplaza 'campo1', 'campo2', 'campo3' con los nombres reales de los campos de tu modelo
admin.site.register(Sitio, SitioAdmin)

admin.site.register(Usuario)

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
    extra = 0  # Ajusta según necesidades

class RegistroPropietarioInline(admin.StackedInline):
    model = RegistroPropietario
    extra = 0

class RegistroPropiedadInline(admin.StackedInline):
    model = RegistroPropiedad
    extra = 0

class RegistroSitioInline(admin.StackedInline):
    model = RegistroSitio
    extra = 0

class RegistroSitioImagenesInline(admin.StackedInline):
    model = RegistroSitioImagenes
    extra = 0

class RegistioElectricoInline(admin.StackedInline):
    model = RegistioElectrico
    extra = 0



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
    # Configuraciones adicionales como list_display, search_fields, etc.
    list_display = ('sitio', 'pais_empresa', 'candidato', 'usuario', )
    
    def pais_empresa(self, obj):
        # Intenta recuperar el objeto Usuario relacionado al user de RegistroLlegada
        try:
            usuario = Usuario.objects.get(user=obj.usuario)
            return usuario.pais_empresa
        except Usuario.DoesNotExist:
            return "No definido"  # O puedes retornar un valor que indique que no se encontró el Usuario

    pais_empresa.short_description = 'País Empresa' 
admin.site.register(RegistroLlegada, RegistroLlegadaAdmin)