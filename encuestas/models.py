""" Modelos de la app de encuestas. """

# Django
from django.db import models

# Utilidades
from utils.models import BaseModel

# Modelos de la app de usuarios
from users.models import User

class Encuesta(BaseModel):
    """ Modelo de encuesta.
    
    Una encuesta es un formulario personalizado creado solo por los usuarios que
    tienen permisos.
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="encuestas", null=True, blank=True)
    nombre = models.CharField('Nombre de la encuesta',max_length=252)
    descripcion = models.TextField('Descripción de la encuesta')
    estado_terminado = models.BooleanField('Encuesta terminada', default=False)
    is_active = models.BooleanField('Encuesta activada', default=False)

    def __str__(self):
        return self.nombre

    def ha_sido_diligenciada(self):
        return RespuestaCampo.objects.filter(encuesta=self, user=self.request.user).exists()

class CampoEncuesta(models.Model):
    """ Modelo del campo de una encuesta. 
    
    Los campos de una encuesta son los campos personalizados que tendrá esta.
    """

    TIPO_TEXTO = 1
    """ Tipo de campo texto. """

    TIPO_FECHA = 2
    """ Tipo de campo fecha. """

    TIPO_LISTA = 3
    """ Tipo de campo lista. """

    TIPO_TEXTO_AREA = 4
    """ Tipo de campo texto área. """

    TIPO_CHOICES = (
        (TIPO_TEXTO, 'Texto'),
        (TIPO_FECHA, 'Fecha'),
        (TIPO_LISTA, 'Lista'),
        (TIPO_TEXTO_AREA, 'Caja de área de texto'),
    )

    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name="campos")
    nombre_campo = models.CharField('Nombre del campo', max_length=252)
    tipo = models.PositiveIntegerField('Tipo de campo', choices=TIPO_CHOICES)
    values_select = models.TextField('Valores de la lista',blank=True, null=True)
    is_required = models.BooleanField('¿Campo requerido?')

    def __str__(self):
        return str("Campo {0} de la encuesta {1}".format(self.nombre_campo, self.encuesta))

class RespuestaCampo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="respuestas")
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name="respuestas")
    pregunta = models.ForeignKey(CampoEncuesta, on_delete=models.CASCADE, related_name="respuestas")
    respuesta = models.CharField(max_length=1024)

    def __str__(self):
        return self.respuesta

