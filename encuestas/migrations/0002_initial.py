# Generated by Django 3.2.11 on 2022-02-14 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('encuestas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestacampo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='respuestas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='encuestas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campoencuesta',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campos', to='encuestas.encuesta'),
        ),
    ]