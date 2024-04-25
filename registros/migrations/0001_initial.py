# Generated by Django 4.2.11 on 2024-04-25 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Candidato",
            fields=[
                (
                    "candidato",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Registro",
                    ),
                ),
                (
                    "fecha_creacion",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Fecha"
                    ),
                ),
            ],
            options={
                "verbose_name": "Registro Campo",
                "verbose_name_plural": "Registros Campo",
            },
        ),
        migrations.CreateModel(
            name="Empresa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pais", models.CharField(max_length=25)),
                ("nombre", models.CharField(max_length=25, verbose_name="Empresa")),
            ],
            options={
                "verbose_name": "Empresa",
                "verbose_name_plural": "Empresas",
            },
        ),
        migrations.CreateModel(
            name="RegistroLlegada",
            fields=[
                (
                    "candidato",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="registros.candidato",
                    ),
                ),
                (
                    "fecha_llegada",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Fecha de llegada",
                    ),
                ),
                ("lat_llegada", models.FloatField(blank=True, null=True)),
                ("lon_llegada", models.FloatField(blank=True, null=True)),
                (
                    "status_llegada",
                    models.CharField(
                        blank=True,
                        choices=[("true", "Llegada"), ("false", "Incidente")],
                        max_length=5,
                        verbose_name="Estatus",
                    ),
                ),
                (
                    "imagen_llegada",
                    models.ImageField(blank=True, null=True, upload_to="llegada/"),
                ),
                ("observaciones", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Llegada",
                "verbose_name_plural": "Llegada",
            },
        ),
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=120)),
                ("telf", models.CharField(max_length=15)),
                (
                    "empresa",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registros.empresa",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Usuario",
                "verbose_name_plural": "Usuarios",
            },
        ),
        migrations.CreateModel(
            name="Sitio",
            fields=[
                (
                    "PTICellID",
                    models.CharField(
                        max_length=15, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("nombre", models.CharField(blank=True, max_length=100)),
                (
                    "lat_nominal",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Latitud Nominal"
                    ),
                ),
                (
                    "lon_nominal",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Longitud Nominal"
                    ),
                ),
                ("altura", models.CharField(blank=True, max_length=10, null=True)),
                ("provincia", models.CharField(blank=True, max_length=25, null=True)),
                ("municipio", models.CharField(blank=True, max_length=25, null=True)),
                ("localidad", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "img_google",
                    models.ImageField(blank=True, null=True, upload_to="imgs_gmap/"),
                ),
                (
                    "contador_llegadas",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Registro/Candidato"
                    ),
                ),
                (
                    "empresa",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sitios",
                        to="registros.empresa",
                    ),
                ),
            ],
            options={
                "verbose_name": "Datos Sitio",
                "verbose_name_plural": "Datos Sitio",
            },
        ),
        migrations.CreateModel(
            name="RegistroSitioImagenes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pic",
                    models.FileField(blank=True, null=True, upload_to="sitios/fotos/"),
                ),
                (
                    "descripcion",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "candidato",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registros.candidato",
                        verbose_name="Registro",
                    ),
                ),
                (
                    "sitio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registros.sitio",
                    ),
                ),
            ],
            options={
                "verbose_name": "Imagen Sitio",
                "verbose_name_plural": "Imagenes Sitio",
            },
        ),
        migrations.AddField(
            model_name="candidato",
            name="sitio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="registros.sitio"
            ),
        ),
        migrations.AddField(
            model_name="candidato",
            name="usuario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="registros.usuario"
            ),
        ),
        migrations.CreateModel(
            name="RegistroSitio",
            fields=[
                (
                    "candidato",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="registros.candidato",
                        verbose_name="Registro",
                    ),
                ),
                (
                    "sitio_fecha",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Fecha de Visita",
                    ),
                ),
                (
                    "sitio_lat",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Latitud Torre"
                    ),
                ),
                (
                    "sitio_lon",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Longitud Torre"
                    ),
                ),
                (
                    "sitio_descripcion",
                    models.TextField(blank=True, null=True, verbose_name="Comentarios"),
                ),
                (
                    "img_google_dist_nominal",
                    models.ImageField(
                        blank=True, null=True, upload_to="sitios/imgs_gmap/"
                    ),
                ),
                (
                    "img_google_sitio",
                    models.ImageField(
                        blank=True, null=True, upload_to="sitios/imgs_gmap/"
                    ),
                ),
                (
                    "sitio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registros.sitio",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sitio",
                "verbose_name_plural": "Sitio",
            },
        ),
        migrations.CreateModel(
            name="RegistroPropietario",
            fields=[
                (
                    "candidato",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="registros.candidato",
                        verbose_name="Registro",
                    ),
                ),
                (
                    "propietario_nombre_apellido",
                    models.CharField(max_length=100, verbose_name="Nombre y Apellido"),
                ),
                (
                    "propietario_born",
                    models.DateTimeField(verbose_name="Fecha de Nacimiento"),
                ),
                (
                    "propietario_ci",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        verbose_name="Documento de Identidad",
                    ),
                ),
                (
                    "propietario_telf",
                    models.CharField(
                        max_length=15, verbose_name="Telefono de Contacto"
                    ),
                ),
                (
                    "propietario_direccion",
                    models.TextField(
                        max_length=100, verbose_name="Direccion Domicilio"
                    ),
                ),
                (
                    "propietario_estado_civil",
                    models.BooleanField(default=True, verbose_name="Estado Civil"),
                ),
                (
                    "sitio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registros.sitio",
                    ),
                ),
            ],
            options={
                "verbose_name": "Propietario",
                "verbose_name_plural": "Propietario",
            },
        ),
        migrations.CreateModel(
            name="RegistroPropiedad",
            fields=[
                (
                    "candidato",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="registros.candidato",
                        verbose_name="Registro",
                    ),
                ),
                ("propiedad_rol", models.CharField(max_length=100, verbose_name="Rol")),
                (
                    "propiedad_escritura",
                    models.CharField(max_length=100, verbose_name="Escritura"),
                ),
                (
                    "propiedad_registro_civil",
                    models.TextField(max_length=100, verbose_name="Registro Civil"),
                ),
                (
                    "propiedad_imagen",
                    models.ImageField(
                        blank=True, null=True, upload_to="sitios/propiedad"
                    ),
                ),
                (
                    "propiedad_descripcion",
                    models.TextField(blank=True, null=True, verbose_name="Comentarios"),
                ),
                (
                    "sitio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registros.sitio",
                    ),
                ),
            ],
            options={
                "verbose_name": "Propiedad",
                "verbose_name_plural": "Propiedad",
            },
        ),
        migrations.CreateModel(
            name="RegistroLocalidad",
            fields=[
                (
                    "candidato",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="registros.candidato",
                        verbose_name="Registro",
                    ),
                ),
                ("provincia", models.CharField(blank=True, max_length=25, null=True)),
                ("municipio", models.CharField(blank=True, max_length=25, null=True)),
                ("localidad", models.CharField(blank=True, max_length=25, null=True)),
                ("energia_localidad", models.BooleanField(default=True)),
                (
                    "sitio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registros.sitio",
                    ),
                ),
            ],
            options={
                "verbose_name": "Localidad",
                "verbose_name_plural": "Localidad",
            },
        ),
        migrations.CreateModel(
            name="RegistioElectrico",
            fields=[
                (
                    "candidato",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="registros.candidato",
                        verbose_name="Registro",
                    ),
                ),
                (
                    "electrico_lat",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Latitud Poste"
                    ),
                ),
                (
                    "electrico_lon",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Longitud Poste"
                    ),
                ),
                (
                    "electrico_no_poste",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Identificacion Poste",
                    ),
                ),
                (
                    "electrico_comentario",
                    models.TextField(blank=True, null=True, verbose_name="Comentario"),
                ),
                (
                    "electrico_imagen1",
                    models.ImageField(upload_to="sitios/", verbose_name="Imagen Poste"),
                ),
                (
                    "electrico_imagen2",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="sitios/",
                        verbose_name="Imagen Electrico",
                    ),
                ),
                (
                    "electrico_img_google",
                    models.ImageField(
                        blank=True, null=True, upload_to="sitios/imgs_gmap/"
                    ),
                ),
                (
                    "sitio",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="registros.sitio",
                    ),
                ),
            ],
            options={
                "verbose_name": "Eléctrico",
                "verbose_name_plural": "Eléctrico",
            },
        ),
    ]
