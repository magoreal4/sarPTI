# Generated by Django 4.2.11 on 2024-04-20 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0007_usuario_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitio',
            name='img_google',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes_mapas/'),
        ),
    ]