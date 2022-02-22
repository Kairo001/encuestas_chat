from encuestas.models import RespuestaCampo
from django import template

register = template.Library()

@register.simple_tag
def ha_sido_diligenciada(encuesta, user):
    print(encuesta)
    print(user)
    return RespuestaCampo.objects.filter(encuesta=encuesta, user=user).exists()