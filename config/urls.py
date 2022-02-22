

from django.contrib import admin
from django.urls import path, include

from config.views import indice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indice, name="indice"),
    path('usuarios/', include('users.urls')),
    path('encuestas/', include('encuestas.urls')),
    path('chatapp/', include('chatapp.urls')),
]
