# Generated by Django 4.2.11 on 2024-04-08 16:49

from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0002_rename_candidado_registrositio_candidato'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrositio',
            name='sitio_fecha',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
    ]
