""" Modelos para la aplicación de usuarios. """

# Django

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

#  Utilities
from utils.models import BaseModel

class MyAccounManager(BaseUserManager):
    " Manejador para perfiles de usuario. "

    def create_user(self, numeroId, nombre1, apellido1, celular, correo, password=None):
        """ Crea un nuevo usuario. """

        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico.')
        
        user = self.model(
            correo = self.normalize_email(correo),
            numeroId = numeroId,
            nombre1 = nombre1,
            apellido1 = apellido1,
            celular = celular
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, numeroId, nombre1, apellido1, celular, correo, password):
        """ Creaa un nuevo usuario con permisos de administración. """

        user = self.create_user(
            correo = self.normalize_email(correo),
            password= password,
            numeroId = numeroId,
            nombre1 = nombre1,
            apellido1 = apellido1,
            celular = celular
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_manager = True

        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """ Modelo de usuario. 
    
    Hereda del modelo abstracto base de Django, cambiando el campo username a 
    email y añadiendo algunos campos extras.

    """

    TIPOS_DE_DOCUMENTOS = [
        ('V', 'Cerificado de nacido vivo'),
        ('R', 'Registro civil'),
        ('T', 'Tarjeta de identidad'),
        ('C', 'Cédula de ciudadanía'),
        ('E', 'Cédula de extranjería'),
        ('P', 'Pasaporte'),
        ('A', 'Adulto sin identificar'),
        ('M', 'Menor sin identificar'),
    ]

    GENERO = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    ]

    tipoId = models.CharField(
        'Tipo de indentificación',
        max_length=1,
        choices=TIPOS_DE_DOCUMENTOS,
        blank=True,
        null=True
    )

    numeroId = models.CharField(
        'Número de identificación',
        max_length=13,
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este número de documento.'
        }
    )

    nombre1 = models.CharField('Primer nombre', max_length=40)

    nombre2 = models.CharField(
        'Segundo nombre',
        max_length=40,
        blank=True
    )

    apellido1 = models.CharField('Primer apellido', max_length=40)

    apellido2 = models.CharField(
        'Segundo apellido',
        max_length=40,
        blank=True
    )

    fechaNac = models.DateField('Fecha de nacimiento', blank=True, null=True)

    genero = models.CharField(
        'Género',
        max_length=1,
        choices=GENERO,
        blank=True
    )

    correo = models.EmailField(
        'Dirección de correo electrónico',
        unique=True,
        error_messages={
            'unique': 'Ya existe un usuario con este correo electrónico.'
        }
    )

    direccion = models.CharField(
        'Dirección de residencia',
        max_length=220,
        blank=True
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{10,12}$',
        message="Número no válido."
    )

    telefono = models.CharField(validators=[phone_regex], max_length=13, blank=True)

    celular = models.CharField(validators=[phone_regex], max_length=13)

    email_verified = models.BooleanField(
        'Veridicado',
        default=False,
        help_text='Establece en verdadero cuando el usuario ha verificado su dirección de email.'
    )

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designa si el usuario puede iniciar sesión en el sitio de administración.',
    )

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designa si este usuario debe ser tratado como activo. '
            'Desmarcar esto en lugar de eliminar cuentas.'
        ),
    )

    is_manager = models.BooleanField(
        'manager status',
        default=False,
        help_text='Designa si el usuario es un gerente o no.'
    )

    objects = MyAccounManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['numeroId', 'nombre1', 'apellido1', 'celular']
    EMAIL_FIELD = 'correo'

    def __str__(self):
        """ Retorna el nombre de usuario. """
        return self.numeroId

    def get_short_name(self):
        """ Retorna el nombre de usuario. """
        return self.nombre1

class UserLogs(BaseModel):
    """ Modelo para poder tener un historial de los datos modificados por cada paciente. """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    metadata = models.TextField()

    nombre1 = models.BooleanField(default=False)

    nombre2 = models.BooleanField(default=False)

    apellido1 = models.BooleanField(default=False)

    apellido2 = models.BooleanField(default=False)

    fechaNac = models.BooleanField(default=False)

    genero = models.BooleanField(default=False)

    correo = models.BooleanField(default=False)

    direccion = models.BooleanField(default=False)

    telefono = models.BooleanField(default=False)

    celular = models.BooleanField(default=False)

    entidad = models.BooleanField(default=False)

    def __str__(self):
        """ Retorna el nombre de usuario. """
        return str(self.pk)
