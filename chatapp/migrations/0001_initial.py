# Generated by Django 3.2.11 on 2022-02-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre de la sala')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]