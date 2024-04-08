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

admin.site.register(Servicio)

admin.site.register(Sitio)

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

admin.site.register(RegistroLlegada, RegistroLlegadaAdmin)