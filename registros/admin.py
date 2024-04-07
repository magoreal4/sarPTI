from django.contrib import admin

from .models import (Servicio, 
                     Usuario, 
                     Sitio, 
                     RegistroLlegada, 
                     RegistroLocalidad,
                     RegistroPropietario,
                     RegistroPropiedad,
                     RegistroSitio,
                     RegistioElectrico
                     )

admin.site.register(Servicio)

admin.site.register(Sitio)

admin.site.register(Usuario)

admin.site.register(RegistroLlegada)

admin.site.register(RegistroLocalidad)

admin.site.register(RegistroPropietario)

admin.site.register(RegistroPropiedad)

admin.site.register(RegistroSitio)

admin.site.register(RegistioElectrico)



