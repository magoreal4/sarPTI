# Generated by Django 4.2.11 on 2024-04-06 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0002_sitio_imagen_llegada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitio',
            name='imagen_llegada',
        ),
        migrations.AddField(
            model_name='registro',
            name='imagen_llegada',
            field=models.ImageField(blank=True, null=True, upload_to='sitios/'),
        ),
    ]
