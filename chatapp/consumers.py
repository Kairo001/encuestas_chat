""" Consumers de Channels.
Los consumers son una abstracción que le permite crear aplicaciones ASGI fácilmente.
Los consumers hacen un par de cosas en particular:
* Estructura el código como una serie de funciones que se llamarán cada vez que ocurra un
evento, en lugar de hacer que escriba un ciclo de enventos.
* Permite escribir código asíncoro o síncrono y se ocupa de tranferencias y subprocesos.

Cuando Channels acepta una conexión WebSocket, consulta la configuración de enrutamiento raíz
para buscar un consumidor y luego llama a varias funciones en el consumidor para manejar eventos
de la conexión.
"""

# Utilidades
import json

# Channels
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# Modelos
from chatapp.models import Message, Room

# Modelos de la app de users
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    """ Consumer de chat.
    Cuando un usuario publica un mensaje, una función de JavaScript transmitirá el mensaje a través de WebSocket a un ChatConsumer,
    este recibirá ese mensaje y lo reenviará al grupo conrrespondiente al nombre de la sala. Cada ChatCosumer en el mismo grupo (y,
    por lo tanto, en la misma sala) recibirá el mensaje del grupo y lo reenviará a través de WebSocket a JavaScript, donde se agre_
    gará al registro de chat.

    Cada consumer tiene un alcanse que contiene información sobre su conexión, incluidos, en particular, los argumentos posicionales
    o de palabras clave de la ruta URL y el usuario autenticado actualmente, si lo hay. 
    """

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Los nombres de grupo solo pueden contener letras, dígitos, guiones y puntos. Por lo tanto, este código fallará en nombres
        # de rooms que tengan otros carácteres.
        self.room_group_name = 'chat_%s' % self.room_name

        # Se une al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Acepta la conexión a WebSocket. Si no se llama a accept() denro del método connect(), la conexión será rechazada y cerrada.
        # Por lo tanto, se debe llamar a accept() como última acción en connect() si se elige aceptar la conexión.
        await self.accept()

    async def disconnect(self, close_code):

        # Abandona el grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data =json.loads(text_data)
        message = data['message']
        numeroId = data['numeroId']
        room = data['room']

        await self.save_message(numeroId, room, message)

        # Envía un evento a un grupo. Un evento tiene una clave especial 'type' que corresponde al nombre del método que se debe invocar
        # en los consummers que reciven el evento. 
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : message,
                'numeroId' : numeroId,
                'room' : room,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        numeroId = event['numeroId']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': message,
            'numeroId': numeroId,
            'room': room
        }))

    @sync_to_async
    def save_message(self, numeroId, room, message):
        user = User.objects.get(numeroId=numeroId)
        room = Room.objects.get(slug=room)

        Message.objects.create(
            user=user,
            room=room,
            content=message
        )