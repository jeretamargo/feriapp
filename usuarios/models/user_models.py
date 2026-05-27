# Create your models here.
from django.db import models


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    TIPO_USUARIO = [
    ("visitante", "Visitante"),
    ("emprendedor", "Emprendedor"),
]

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO
    )
    pass

"""
El modelo User en django ya existe y trae muchas caracteristicas ya implementadas, bajo ningun concepto conviene reinventarlo, por lo que se extiende con AbstractUser para agregarle el campo Notificacion
"""