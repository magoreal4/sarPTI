from django.db import models
from django.contrib.auth.models import User




class Empresa(models.Model):
    pais = models.CharField(max_length=25, blank=True, null=True)
    nombre = models.CharField("Empresa", max_length=25, blank=True, null=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f"{self.nombre} - {self.pais}"


class Sitio(models.Model):
    PTICellID = models.CharField(
        max_length=17,
        unique=True,
        primary_key=True
    )
    nombre = models.CharField(max_length=100, blank=True)
    lat_nominal = models.FloatField(blank=True, null=True, verbose_name='Latitud Nominal')
    lon_nominal = models.FloatField(blank=True, null=True, verbose_name='Longitud Nominal')
    altura = models.CharField(max_length=10, blank=True, null=True)
    provincia = models.CharField("Provincia/Region", max_length=25, blank=True, null=True)
    municipio = models.CharField(max_length=25, blank=True, null=True)
    localidad = models.CharField("Localidad/Comuna", max_length=25, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, related_name='sitios', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sitios', blank=True, null=True)

    img_google = models.ImageField(upload_to='imgs_gmap/', null=True, blank=True)
    contador_llegadas = models.PositiveIntegerField("Reg./Cand.", default=0)
    
    def __str__(self):
        return self.PTICellID

    class Meta:
        verbose_name = "Sitio"
        verbose_name_plural = "Sitios"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telf = models.CharField(max_length=15)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

