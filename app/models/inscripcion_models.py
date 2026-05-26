from __future__ import annotations

from django.db import models

from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User
from app.models.feria_models import Feria



class Inscripcion(models.Model):

    ESTADOS = [
        #   para que pongan de las dos maneras
        ("confirmada", "Confirmada"),
        ("lista_espera", "Lista de espera"),
        ("cancelada", "Cancelada"),
    ]

    emprendedor = models.ForeignKey(
        Emprendedor,
        on_delete=models.CASCADE
    )

    feria = models.ForeignKey(
        Feria,
        on_delete=models.CASCADE
    )

    numero_puesto = models.PositiveIntegerField()

    fecha_inscripcion = models.DateField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="confirmada"
    )

    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    class Meta:
        unique_together = ("feria", "numero_puesto")

    def __str__(self):
        return f"{self.emprendedor} - {self.feria}"

    @classmethod
    def validate(cls, feria, emprendedor, numero_puesto, estado):
        errors = []

        if not feria:
            errors.append("La feria es obligatoria.")

        if not emprendedor:
            errors.append("El emprendedor es obligatorio.")

        if numero_puesto is None or numero_puesto <= 0:
            errors.append("El número de puesto debe ser mayor a cero.")

        estados_validos = [e[0] for e in cls.ESTADOS]

        if estado not in estados_validos:
            errors.append("Estado inválido.")

        return errors
    
    @classmethod
    def new(cls, feria, emprendedor, numero_puesto, estado="confirmada"):
        errors = cls.validate(
            feria,
            emprendedor,
            numero_puesto,
            estado
        )

        if errors:
            return None, errors

        inscripcion = cls.objects.create(
            feria=feria,
            emprendedor=emprendedor,
            numero_puesto=numero_puesto,
            estado=estado
        )

        return inscripcion, []
    
    def update(self, numero_puesto, estado):
        errors = self.__class__.validate(
            self.feria,
            self.emprendedor,
            numero_puesto,
            estado
        )

        if errors:
            return errors

        self.numero_puesto = numero_puesto
        self.estado = estado
        self.save()

        return []
