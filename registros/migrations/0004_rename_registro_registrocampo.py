# Generated by Django 4.2.11 on 2024-04-07 03:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registros', '0003_remove_sitio_imagen_llegada_registro_imagen_llegada'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Registro',
            new_name='RegistroCampo',
        ),
    ]