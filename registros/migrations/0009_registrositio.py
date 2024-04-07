# Generated by Django 4.2.11 on 2024-04-07 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registros', '0008_registropropiedad'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroSitio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sitio_lat', models.FloatField(blank=True, null=True)),
                ('sitio_lon', models.FloatField(blank=True, null=True)),
                ('sitio_imagen', models.ImageField(blank=True, null=True, upload_to='sitios/')),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sitio_candidato', to='registros.registropropietario')),
                ('sitio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sitio_sitio', to='registros.sitio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sitio_usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]