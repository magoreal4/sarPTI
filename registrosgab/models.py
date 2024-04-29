from django.db import models
from registros.models import RegistroLlegada, RegistroPropietario
from registros.models import RegistroSitio 
from django.utils.html import format_html

ZONA_CHOICES = (
    ('u', 'Urbana'),
    ('r', 'Rural'),
)

class RegistroInicio(models.Model):
    candidato_registro = models.OneToOneField(
        RegistroLlegada, 
        primary_key=True,
        on_delete=models.CASCADE,
        verbose_name="Registro",
        )
    candidato_letra = models.CharField("Candidato", max_length=1)
    radio_busqueda = models.PositiveIntegerField()
    tipo_solucion = models.CharField("Tipo de Solución", max_length=2500)
    zona = models.CharField("Zona", max_length=10, default='Urbana', choices=ZONA_CHOICES)
    ASNM = models.PositiveIntegerField("ASNM Terreno", blank=True, null=True)
    contactos_ingreso = models.TextField("Contactos para ingresar al sitio", blank=True, null=True)
    ruta_acceso = models.TextField("Descripción del acceso", null=True)
    ruta_huella = models.TextField("Descripción de la huella proyectada", null=True)
    inf_adicional = models.TextField("Información Adicional", blank=True, null=True)
    
    def __str__(self):
        return f"{self.candidato_registro}"
    
    class Meta:
        verbose_name = "Registro Gabinete"
        verbose_name_plural = "Registro Gabinete"
    
class Imagenes(models.Model):
    registro_inicio = models.ForeignKey(
        RegistroInicio, 
        on_delete=models.CASCADE,
        verbose_name="Registro",
        ) 
    imagen = models.ImageField(upload_to='gabinete/imgs/')
    descripcion = models.CharField(max_length=100)
    
    def image_tag_pic(self):
        return format_html('<img src="{}" width="80" height="auto"/>', self.imagen.url)
    image_tag_pic.short_description = 'Imagen Sitio'

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"
       
class InformacionGeneral(models.Model):
    registro_inicio = models.OneToOneField(
        RegistroInicio, 
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Registro",
        ) 

    fecha_visita = models.DateTimeField("Fecha de visita", blank=True, null=True)
    propietario = models.CharField(max_length=100, blank=True, null=True)
    propietario_telf = models.CharField("Teléfono", max_length=100, blank=True, null=True)
    propietario_direccion = models.CharField("Dirección", max_length=100, blank=True, null=True)
    propietario_email = models.EmailField("Correo Electrónico", blank=True, null=True)
    estado_civil = models.CharField(max_length=100, blank=True, null=True)  
    
    class Meta:
        verbose_name = "Propietario"
        verbose_name_plural = "Propietario"
            

class InformacionPropiedad(models.Model):
    registro_inicio = models.OneToOneField(
        RegistroInicio, 
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Registro",
        ) 
    propiedad_hipoteca = models.BooleanField("Propiedad con Hipoteca", default=False)
    estado_impuestos = models.BooleanField("Impuestos Municipales al dia", default=True)
    apreciaciones = models.TextField(blank=True, null=True, help_text="Apreciaciones preliminares del dueño sobre el alquiler de la propiedad")
    tiempo_negociado = models.CharField("Tiempo negociado (años)", max_length=2, blank=True, null=True)   
    comentarios = models.TextField("Comentarios Adicionales", blank=True, null=True)
    
    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedad"
        
    def __str__(self):
        return f"{self.registro_inicio}"

class Croquis(models.Model):
    registro_inicio = models.OneToOneField(
        RegistroInicio, 
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Registro",
        ) 
    croquis = models.ImageField(upload_to='croquis', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def image_tag_pic(self):
        return format_html('<img src="{}" width="80" height="auto"/>', self.croquis.url)
    image_tag_pic.short_description = 'Croquis'

    class Meta:
        verbose_name = "Croquis"
        verbose_name_plural = "Croquis"
        
class InfTecPropiedad(models.Model):
    registro_inicio = models.OneToOneField(
        RegistroInicio, 
        on_delete=models.CASCADE,
        primary_key=True
        ) 
    dim_frente = models.CharField("Frente (m.)",max_length=10, blank=True, null=True)
    dim_largo = models.CharField("Largo (m.)", max_length=10, blank=True, null=True)
    dim_ampliar = models.CharField("Dimensiones disponibles para ampliar",max_length=10, blank=True, null=True)  
    area = models.CharField("Area (m2)",max_length=10, blank=True, null=True)   
    
    forma_terreno = models.CharField("Forma del Terreno", max_length=255, blank=True, null=True,
                                     help_text="Rectangular, otro (indicar)")  
    topografia_terreno = models.CharField("Topografia del Terreno", max_length=255, blank=True, null=True)
    uso_terreno = models.CharField(max_length=255, blank=True, null=True)
    desc_acceso_sitio = models.TextField("Descripción de Acceso al Sitio", blank=True, null=True,
                                         help_text="Público, acceso controlado, otros")
    material_terreno = models.CharField(max_length=255, blank=True, null=True)
    
    dim_acceso = models.CharField("Ancho & Longitud", max_length=255, blank=True, null=True,
                                  help_text="Dimensiones acceso/carretera/huella (ancho x largo)")  
    condiciones_acceso = models.CharField(max_length=255, blank=True, null=True)    
    tipo_carretera = models.CharField(max_length=255, blank=True, null=True)
    acceso_sitio = models.CharField("Tipo de Vehiculo 4x4, 4x42, otros", max_length=255, blank=True, null=True)
    cond_acceso_equipo = models.TextField("Condiciones Acceso Equipo (gruas, camiones, etc)", blank=True, null=True)
    
    desc_const_aledanas = models.TextField("Descripción Construcciones",blank=True, null=True,
                                           help_text="Descripción construcciones colindantes alrededor del sitio y cercania")  
    desc_const_importantes = models.TextField("Descripción y ubicación construcciones importantes",blank=True, null=True,
                                              help_text="Descripción y ubicación Ubicación de construcciones importantes cercanas y distancia a éstas : aeropuertos, muelles, edificios, escuelas, colegios, centros de salud, centros comerciales, etc.")
    riesgo_inundaciones = models.BooleanField(default=False)
    consideraciones_ambientales = models.TextField("Consideraciones Ambioerales", blank=True, null=True,
                                                   help_text="Consideraciones ambientales : ubicación de ríos, quebradas, nacientes, mantos acuíferos, reservas forestales, derrumbes, etc.")
    
    obras_civiles_especiales = models.TextField("Obras Civiles Especiales y/o Adicionales", blank=True, null=True)  
    
    demoliciones = models.BooleanField(default=False)
    mov_tierras = models.BooleanField("Movimiento de Tierras", default=False)
    muros_contencion = models.BooleanField("Muros de Contención", default=False)
    tala_arboles = models.CharField(max_length=255, blank=True, null=True)
    cons_camino = models.CharField("Construcción huella", max_length=255, blank=True, null=True)
    const_tendido_electrico = models.CharField("Construcción Tendido Electrico",max_length=255, blank=True, null=True)
    colocacion_postes = models.CharField("Colocación de Postes",max_length=255, blank=True, null=True)
    instalacion_transformador = models.CharField(max_length=255, blank=True, null=True) 
    canalizacion_subterranea = models.CharField(max_length=255, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)

    proveedor_agua = models.CharField("Proveedor de Agua", max_length=255, blank=True, null=True)
    proveedor_electrico = models.CharField("Proveedor Energía Electrica", max_length=255, blank=True, null=True)
    no_medidor = models.CharField("Número de Medidor", max_length=255, blank=True, null=True)    
    ubicacion_tendido_electrico = models.CharField(max_length=255, blank=True, null=True)   
    transformador_capacidad = models.CharField(max_length=255, blank=True, null=True)   
    transformador_distancia = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Inf. Técnica"
        verbose_name_plural = "Inf. Técnica"
    
class Documentos(models.Model):
    registro_inicio = models.ForeignKey(
        RegistroInicio, 
        on_delete=models.CASCADE,
        ) 
    documento = models.ImageField(upload_to='documentos', blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Documentos"
        verbose_name_plural = "Documentos"
    
    
    
    
    