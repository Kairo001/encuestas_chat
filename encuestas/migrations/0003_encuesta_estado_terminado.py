# Generated by Django 3.2.11 on 2022-02-16 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encuestas', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuesta',
            name='estado_terminado',
            field=models.BooleanField(default=False, verbose_name='Encuesta terminada'),
        ),
    ]