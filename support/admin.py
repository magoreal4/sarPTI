from django.contrib import admin
from .models import SupportQuery

class SupportQueryAdmin(admin.ModelAdmin):
    # Deshabilitar las opciones de agregar y modificar
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # Hacer que los registros sean solo de lectura
    readonly_fields = ('name', 'email', 'message', 'created_at')

    # Opcional: Personaliza los campos que se mostrarán en la lista
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

# Registrar el modelo con la configuración del admin personalizada
admin.site.register(SupportQuery, SupportQueryAdmin)
