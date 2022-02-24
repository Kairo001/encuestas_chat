""" Consumers de la app de encuestas. """

# Utilidades
import json

# Channels
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from encuestas.models import CampoEncuesta


class NotificationEncuestaConsumer(AsyncWebsocketConsumer):
    """ Consumer de encuesta. """

    async def connect(self):

        self.room_group_name = 'notificar_encuestas'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data =json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'send_message',
                'message' : message
            }
        )

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))

class RealizarEncuestaConsumer(AsyncWebsocketConsumer):
    """ Consumer para poder realizar encuesta. """

    async def connect(self):
        self.encuesta_id = self.scope['url_route']['kwargs']['encuesta_id']

        self.room_group_name = 'encuesta_%s' % self.encuesta_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data =json.loads(text_data)
        pregunta_id = data['pregunta_id']
        checked = data['cheked']

        print(pregunta_id)
        print(checked)

        if pregunta_id != "Encuesta terminada" and checked != "Encuesta terminada":
            print("Actualizando estado de la pregunta")
            await self.update_pregunta(pregunta_id, checked)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'send_message',
                'pregunta_id' : pregunta_id,
                'checked': checked
            }
        )

    async def send_message(self, event):
        pregunta_id = event['pregunta_id']
        checked = event['checked']

        await self.send(text_data=json.dumps({
            'pregunta_id': pregunta_id,
            'checked': checked
        }))

    @sync_to_async
    def update_pregunta(self, pregunta_id, checked):
        pregunta = CampoEncuesta.objects.get(pk=pregunta_id)
        pregunta.is_active = checked
        pregunta.save()