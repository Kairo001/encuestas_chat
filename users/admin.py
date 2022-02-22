from django.contrib import admin

# Modelos
from .models import User, UserLogs

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'numeroId',
        'correo',
        'nombre1',
        'apellido1',
    )

@admin.register(UserLogs)
class UserLogsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'metadata',
    )