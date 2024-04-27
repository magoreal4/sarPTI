# Generated by Django 4.2.11 on 2024-04-27 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("registros", "0008_alter_registropropietario_usuario"),
    ]

    operations = [
        migrations.AddField(
            model_name="registropropiedad",
            name="usuario",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="registropropiedad",
            name="propiedad_descripcion",
            field=models.TextField(default=1, verbose_name="Comentarios"),
            preserve_default=False,
        ),
    ]
