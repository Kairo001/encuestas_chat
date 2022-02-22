""" Enrutamiento para la app de chat. """

# Django
from django.urls import path

# Consummers
from chatapp import consumers

websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    # Se llama al método de clase as_asgi() para obtener una aplicación ASGI que creará una instancia
    # del consumidor para cada conexión del usuario.
]

