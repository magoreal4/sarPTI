from django.db import models
from solo.models import SingletonModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class SiteConfiguration(SingletonModel):
    logo = models.ImageField(upload_to='logo', blank=True, null=True)
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
    
    def __str__(self):
        return "Configuración"

    class Meta:
        verbose_name = "Configuración"
    

    