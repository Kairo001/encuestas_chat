""" Configuración de enrutamiento raíz. 
Esta configuración de enrutamiento raíz especifica que cuando se realiza una conexión a el servidor
de desarrollo de Channels, ProtocolTypeRouter primero inspecciona el tipo de conexión y si se trata
de una conexión WebSocket(ws:///  wss://), la conexión se le dará al AuthMiddlewareStack 
"""

import os

# Channels
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Django
from django.urls import path
from django.core.asgi import get_asgi_application

# Enrutamiento
from encuestas import consumers as consumers_encuestas
from chatapp import consumers as consumers_chatapp

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/realizar_encuesta/<encuesta_id>/', consumers_encuestas.RealizarEncuestaConsumer.as_asgi()),
            path('ws/notificar_encuesta/', consumers_encuestas.NotificationEncuestaConsumer.as_asgi()),
            path('ws/<str:room_name>/', consumers_chatapp.ChatConsumer.as_asgi()),
        ])
    ),
})
