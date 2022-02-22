""" Enrutamiento para la app de encuestas. """

# Django
from django.urls import path

# Consummers
from encuestas import consumers

websocket_urlpatterns = [
    path('ws/notificar_encuesta/', consumers.NotificationEncuestaConsumer.as_asgi()),
]