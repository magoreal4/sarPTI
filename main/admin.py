from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from solo.admin import SingletonModelAdmin
from configapp.models import SiteConfiguration
from django.forms import PasswordInput
from django.utils.html import format_html
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Empresa, Sitio
from django import forms
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class MyAdminSite(AdminSite):    
    def get_app_list(self, request, app_label=None):
        # Obtener la lista original de aplicaciones y modelos
        app_list = super().get_app_list(request, app_label)
        # Aquí puedes definir el orden deseado para cada aplicación
        app_orders = {
            'main': ['Empresa', 'Sitio'], 
            'registros': ['Candidato', 'RegistroLlegada', 'RegistroLocalidad',
                          'RegistroPropietario', 'RegistroPropiedad', 'RegistroSitio',
                          'RegistroSitioImagenes', 'RegistioElectrico'],
            'registrosgab': ['RegistroInicio', 'Imagenes', 'InformacionGeneral',
                             'InformacionPropiedad', 'Croquis', 'InfTecPropiedad', 'Documentos'],
            'admin_interface.theme': ['Theme'],
            # 'another_app': ['AnotherModel1', 'AnotherModel3', 'AnotherModel2']
        }

        # Reordenar los modelos de cada aplicación según el orden definido
        for app in app_list:
            app_name = app['app_label']
            model_order = app_orders.get(app_name, [])
            app['models'].sort(key=lambda x: model_order.index(x['object_name']) if x['object_name'] in model_order else float('inf'))

        return app_list
		
admin.site = MyAdminSite(name='myadmin')



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Buscador'

    # def get_readonly_fields(self, request, obj=None):
    #     if not request.user.is_superuser:
    #         return self.readonly_fields + ('empresa',)
    #     return self.readonly_fields


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'first_name', 'last_name', 'get_telefono', 'email', )
    list_filter = ()

    def get_telefono(self, obj):
        return obj.userprofile.telf if obj.userprofile else None
    get_telefono.short_description = 'Telefono'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(userprofile__empresa=request.user.userprofile.empresa)
        return qs


admin.site.register(User, UserAdmin)

admin.site.register(Group, GroupAdmin)


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('pais', 'nombre')


admin.site.register(Empresa, EmpresaAdmin)


# SITIOS
class SitiosResource(resources.ModelResource):
    class Meta:
        model = Sitio
        import_id_fields = ('PTICellID',)


class SitioAdmin(ImportExportModelAdmin):
    resource_class = SitiosResource
    list_display = ('PTICellID',
                    'nombre',
                    'altura',
                    'empresa',
                    'usuario',
                    'contador_llegadas',
                    # 'img_thumbnail'
                    )
    # list_editable = 
    readonly_fields = ('img_thumbnail', )
    fields = (
        'PTICellID',
        'nombre',
        'lat_nominal',
        'lon_nominal',
        'altura',
        'provincia',
        'municipio',
        'localidad',
        'empresa',
        'usuario',
        # 'img_google',
        'contador_llegadas',
        'img_thumbnail'
    )
    
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return self.readonly_fields + ('empresa',)

    def get_list_editable(self, request):
        if request.user.is_superuser:
            return ('empresa', 'usuario')
        return ('usuario',)
    
    def changelist_view(self, request, extra_context=None):
        # Ajustar list_editable basado en el usuario antes de mostrar la vista de lista
        self.list_editable = self.get_list_editable(request)
        return super(SitioAdmin, self).changelist_view(request, extra_context)

    
    # Para que solo se vean lo usuarios que pertencen a la empresa
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('main.view_empresa_sites'):
            return qs
        if request.user.userprofile.empresa:
            return qs.filter(empresa=request.user.userprofile.empresa)
        return qs.none()

    def img_thumbnail(self, obj):
        if obj.img_google:
            return format_html('<img src="{}" width="320"  />', obj.img_google.url)
        else:
            return "No hay imagen"
    img_thumbnail.short_description = 'Ubicacion Preview'


admin.site.register(Sitio, SitioAdmin)



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

    # readonly_fields = ['logo_img']
    fields = ('logo',  'api_key')

admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
