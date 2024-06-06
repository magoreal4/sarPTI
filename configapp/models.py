from django.db import models
from solo.models import SingletonModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from markdownx.models import MarkdownxField


class PolicyDocument(SingletonModel):
    title = models.CharField(max_length=100)
    content = MarkdownxField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'politica de privacidad'
        verbose_name_plural = 'politica de privacidad'

class TermsConditions(SingletonModel):
    title = models.CharField(max_length=100)
    content = MarkdownxField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'terminos y condiciones'
        verbose_name_plural = 'terminos y condiciones'

# Sobrescribe el sistema de almacenamiento para permitir la sobreescritura de archivos
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Si el archivo ya existe, se elimina antes de guardar uno nuevo
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name  # Retorna el nombre original sin agregar caracteres adicionales


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Extrae la extensión del archivo
    valid_extensions = ['.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension. Only PNG files are allowed.')


def get_fixed_filename(instance, filename):

    return os.path.join('admin-interface/logo/', "logo3_COClnvn.png")

class SiteConfiguration(SingletonModel):
    logo = models.ImageField(
        upload_to=get_fixed_filename, 
        storage=OverwriteStorage(), 
        validators=[validate_file_extension],
        help_text="Solo archivos png")
    logo_thumbnail = ImageSpecField(source='logo',
                                processors=[ResizeToFill(100, 100)],
                                format='JPEG',
                                options={'quality': 60})
    api_key = models.CharField(
        "API Key de Google Maps", 
        max_length=100, 
        blank=True, 
        null=True,
        help_text="API Key de Google Maps, para generar imagenes satelitales en los reporte",
        )
    recipients = models.TextField("Destinarios", default="soporte@btspti.com", help_text="Ingrese correos electrónicos separados por comas")
    
    
    def save(self, *args, **kwargs):
        # Cambia el nombre del archivo cada vez que se guarda el modelo
        self.logo.name = get_fixed_filename(self, self.logo.name)
        super(SiteConfiguration, self).save(*args, **kwargs)
    
    def set_api_key(self, raw_api_key):
        self.api_key = make_password(raw_api_key)
        self.save()

    def check_api_key(self, raw_api_key):
        return check_password(raw_api_key, self.api_key)
    
    def __str__(self):
        return "Configuración"

    class Meta:
        verbose_name = "Configuración"
    
class ApkFile(models.Model):
    name = models.CharField(max_length=25)
    file = models.FileField(upload_to='apks/')
    
    def __str__(self):
        return self.name