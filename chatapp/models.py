""" Modelos de la app de chat. """

# Django
from django.db import models

# Modelos de la app de users
from users.models import User


class Room(models.Model):
    nombre =  models.CharField('Nombre de la sala',max_length=255)
    slug = models.SlugField(unique=True)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created = models.DateTimeField(
        'create at',
        auto_now_add=True,
        help_text='Fecha y hora en la cual el mensaje fue creado.'
    )

    class Meta:
        ordering = ['created']