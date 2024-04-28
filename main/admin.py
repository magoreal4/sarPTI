from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration
from django.forms import PasswordInput
from django.utils.html import format_html

class MyAdminSite(admin.AdminSite):
    site_header = 'BTS PTI'
    site_title = 'BTS PTI'
    index_title = 'Inicio'

    class Media:
        # js = ('js/admin_custom.js',)
        css = {
             'all': ('css/custom_admin.css',),
        }
    
    def get_app_list(self, request):
        # Obtener la lista original de aplicaciones y modelos
        app_list = super().get_app_list(request)

        # Definir el orden deseado para las aplicaciones
        app_order = ['registros', 'main', 'auth']

        # Configuración de orden personalizado y agrupación para 'registros'
        custom_order = {
            'registros': {
                'Grupo1': ['Empresa', 'Usuario', 'Sitio'],
                'Grupo2': ['Candidato',],
                'Grupo3': [
                    'RegistroLlegada',
                    'RegistroLocalidad', 
                    'RegistroPropietario', 
                    'RegistroPropiedad',
                    'RegistroSitio',
                    'RegistroSitioImagenes',
                    'RegistioElectrico'
                ]
            },
            # 'main': {
            #     'Grupo4': ['SiteConfiguration'],
            # }
            # 'main': {
            #     'Grupo4': ['SiteConfiguration'],
            # }
            # 'auth': {
            #     'Usuarios': ['User', 'Group'],  # Asumiendo que quieres agrupar User y Group
            # }
        }
        subtitles = {
            'registros': {
                'Grupo1': 'Datos del Proyecto',
                'Grupo2': 'Registros',
                'Grupo3': 'Detalle de Registros de campo',
            },
            # 'main': {
            #     'Grupo4': 'Configuración',
            # }
            # 'auth': {
            #     'Usuarios': 'CONTROL DE ACCESO'
            # }
        }

        # Títulos personalizados para las aplicaciones
        custom_titles = {
            'registros': 'Sistema de Registros',
            'main': 'Configuración',
        }

        # Reordenar la lista de aplicaciones según el orden definido
        app_list = sorted(app_list, key=lambda x: app_order.index(x['app_label']) if x['app_label'] in app_order else len(app_order))

        # Reorganizar, renombrar y agrupar los modelos según el orden personalizado
        for app in app_list:
            if app['app_label'] in custom_order:
                # Cambiar el título del menú
                app['name'] = custom_titles.get(app['app_label'], app['name'])

                # Reordenar los modelos de acuerdo al orden personalizado
                ordered_models = []
                # Procesar cada grupo
                for group_name, model_names in custom_order[app['app_label']].items():
                    group_models = []
                    # Agregar subtítulo si existe uno definido para el grupo
                    if group_name in subtitles[app['app_label']]:
                        group_models.append({'name': subtitles[app['app_label']][group_name], 'is_subtitle': True})
                    for model_name in model_names:
                        for model in app['models']:
                            if model['object_name'] == model_name:
                                group_models.append(model)
                    ordered_models.extend(group_models)
                app['models'] = ordered_models

        return app_list

admin.site = MyAdminSite(name='myadmin')

admin.site.register(User, UserAdmin)

admin.site.register(Group, GroupAdmin)

from django import forms

class SingletonAdminForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        widgets = {
            'api_key': PasswordInput(render_value=True),  # Muestra el campo como de tipo contraseña
        }
        
class SiteConfigurationAdmin(SingletonModelAdmin):
    form = SingletonAdminForm
#     form = ConfiguracionForm
    def logo_img(self, obj):
        if obj.logo_thumbnail:
            return format_html('<img src="{}" width="100" height="100" />', obj.logo_thumbnail.url)
        else:
            return "No hay imagen"
    logo_img.short_description = 'Logo Preview'

    readonly_fields = ['logo_img']
    fields = ('logo', 'logo_img', 'api_key')

admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
