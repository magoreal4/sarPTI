from django.db import models

class Principal(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    

    