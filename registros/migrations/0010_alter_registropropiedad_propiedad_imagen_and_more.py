# Generated by Django 4.2.11 on 2024-04-27 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("registros", "0009_registropropiedad_usuario_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registropropiedad",
            name="propiedad_imagen",
            field=models.ImageField(null=True, upload_to="sitios/propiedad"),
        ),
        migrations.AlterField(
            model_name="registrositio",
            name="sitio_descripcion",
            field=models.TextField(default=1, verbose_name="Comentarios"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="registrositio",
            name="sitio_fecha",
            field=models.DateTimeField(verbose_name="Fecha de Visita"),
        ),
        migrations.AlterField(
            model_name="registrositio",
            name="sitio_lat",
            field=models.FloatField(default=1, verbose_name="Latitud Torre"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="registrositio",
            name="sitio_lon",
            field=models.FloatField(default=1, verbose_name="Longitud Torre"),
            preserve_default=False,
        ),
    ]
