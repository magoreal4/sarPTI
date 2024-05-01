from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from solo.admin import SingletonModelAdmin
from configapp.models import SiteConfiguration
from django.forms import PasswordInput
from django.utils.html import format_html
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    def get_app_list(self, request):
        # Obtener la lista original de aplicaciones y modelos
        app_list = super().get_app_list(request)
        # Aquí puedes definir el orden deseado para cada aplicación
        app_orders = {
            'main': ['Empresa', 'Sitio', ], 
            'registros': ['Candidato',
                          'RegistroLlegada',
                          'RegistroLocalidad',
                          'RegistroPropietario',
                          'RegistroPropiedad',
                          'RegistroSitio',
                          'RegistroSitioImagenes',
                          'RegistioElectrico',
                          ],
            'registrosgab': ['RegistroInicio',
                             'Imagenes',
                             'InformacionGeneral',
                             'InformacionPropiedad',
                             'Croquis',
                             'InfTecPropiedad',
                             'Documentos',
                             ]
            # 'another_app': ['AnotherModel1', 'AnotherModel3', 'AnotherModel2']
        }

        # Reordenar los modelos de cada aplicación según el orden definido
        for app in app_list:
            app_name = app['app_label']
            if app_name in app_orders:
                app['models'].sort(key=lambda x: app_orders[app_name].index(x['object_name']))

        return app_list

# Reemplaza el sitio admin predeterminado por el personalizado
admin.site = MyAdminSite(name='myadmin')

# class MyAdminSite(admin.AdminSite):
#     site_header = 'BTS PTI'
#     site_title = 'BTS PTI'
#     index_title = 'Inicio'

#     def get_app_list(self, request):
#         # Obtener la lista original de aplicaciones y modelos
#         app_list = super().get_app_list(request)

#         # Definir el orden deseado para las aplicaciones
#         app_order = ['registros', 'registrosgab', 'main', 'auth']

#         # Configuración de orden personalizado para los modelos dentro de cada aplicación
#         custom_order = {            
#             'registros': [
#                 'Empresa', 'Usuario', 'Sitio', 'Candidato', 'RegistroLlegada',
#                 'RegistroLocalidad', 'RegistroPropietario', 'RegistroPropiedad',
#                 'RegistroSitio', 'RegistroSitioImagenes', 'RegistioElectrico'
#             ],
#             'registrosgab': [
#                 'RegistroInicio', 'Imagenes', 'InformacionGeneral', 'InformacionPropiedad',
#                 'Croquis', 'InfTecPropiedad', 'Documentos'
#             ],
#         }

#         # Títulos personalizados para las aplicaciones
#         custom_titles = {
#             'registros': 'Registros Campo',
#             'registrosgab': 'Registros Gabinete',
#             'main': 'Configuración',
#         }

#         # Reordenar la lista de aplicaciones según el orden definido
#         app_list = sorted(app_list, key=lambda x: app_order.index(x['app_label']) if x['app_label'] in app_order else len(app_order))

#         # Reorganizar y renombrar los modelos según el orden personalizado
#         for app in app_list:
#             if app['app_label'] in custom_order:
#                 # Cambiar el título del menú
#                 app['name'] = custom_titles.get(app['app_label'], app['name'])

#                 # Reordenar los modelos de acuerdo al orden personalizado
#                 ordered_models = []
#                 model_names = custom_order[app['app_label']]
#                 for model_name in model_names:
#                     for model in app['models']:
#                         if model['object_name'] == model_name:
#                             ordered_models.append(model)
#                 app['models'] = ordered_models

#         return app_list


    


# admin.site = MyAdminSite(name='myadmin')

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
