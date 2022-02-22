""" Urls de la app de chat. """

#Django
from django.urls import path

# Vistas
from chatapp import views

urlpatterns = [
    path('rooms/', views.RoomsTemplateView.as_view(), name="rooms"),
    path('room/<slug:slug>/', views.RoomTemplateView.as_view(), name="room"),
    path('messages/<slug>/', views.MessagesView.as_view(), name='get_messages')
]