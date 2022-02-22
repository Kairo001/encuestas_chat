""" Modelos de utilidad. """

# Django
from django.db import models

class BaseModel(models.Model):
    """ Modelo base.
    
    BaseModel actúa como una clase base abstracta de la que heredarán todos los demás modelos del proyecto. 
    Esta clase proporciona a cada tabla los siguientes atributos:

         + created (DateTime): Almacena la fecha y hora en que se creó el objeto.
         + modified (DateTime): Almacena la última fecha y hora en que se modificó el objeto.
    """

    created = models.DateTimeField(
        'create at',
        auto_now_add=True,
        help_text='Fecha y hora en la cual el objeto fue creado.'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Fecha y hora de la última modificación del objeto.'
    )

    class Meta:
        """ Opciones Meta. """
        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']