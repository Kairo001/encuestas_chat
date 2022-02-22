""" Registro de los modelos en el panel de administración de Django. """

from django.contrib import admin


from chatapp.models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
    )