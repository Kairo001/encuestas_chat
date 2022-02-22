""" Vistas de la app de chat. """

#Django
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

# Modelos
from chatapp.models import Room, Message

class RoomsTemplateView(LoginRequiredMixin, TemplateView):
    """ Vista para seleccionar la sala de chat. """

    login_url = 'login'
    template_name = "chatapp/rooms.html"

    def get_context_data(self, **kwargs):

        context = super(RoomsTemplateView, self).get_context_data(**kwargs)

        rooms = Room.objects.all()
        context['rooms'] = rooms

        return context

class RoomTemplateView(LoginRequiredMixin, TemplateView):
    """ Vista del chat de la sala seleccionada. """

    login_url = 'login'
    template_name = "chatapp/room.html"

    def get_context_data(self, **kwargs):

        context = super(RoomTemplateView, self).get_context_data(**kwargs)
        room = Room.objects.get(slug=self.kwargs['slug'])
        messages = Message.objects.filter(room=room)[0:25]
        context['messages'] = messages
        context['room'] = room

        return context

class MessagesView(ListView):
    paginate_by = 3
 
    def get_queryset(self, *args, **kwargs):
        room = Room.objects.get(slug=self.kwargs['slug'])
        queryset = Message.objects.filter(room=room).order_by('-created')
        return queryset
 
    def get(self, *args, **kwargs):
        # Validation and authentication 
        response = {}
        response['success'] = True
        paginator = self.get_paginator(self.get_queryset(), self.paginate_by)
        if int(self.request.GET.get('page', 1)) > paginator.num_pages:
            response['success'] = False
            return JsonResponse(response)
        template_response = super().get(*args, **kwargs)
        context_data = self.get_context_data()
        message_list = context_data['object_list']
        message_json_list = []
        for message in message_list:
            message_json = {}
            message_json['content'] = message.content
            message_json['created'] = timezone.localtime(
                message.created).strftime('%Y-%m-%d %H:%M')
            message_json['user'] = message.user.numeroId
            message_json['nombre'] = '{} {}'.format(message.user.nombre1, message.user.apellido2)
            message_json_list.append(message_json)
        response['messages'] = message_json_list[::-1]
        return JsonResponse(response)