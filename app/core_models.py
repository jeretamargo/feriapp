"""Modelos de dominio para la aplicación de ferias."""

from __future__ import annotations

from django.db import models

from usuarios.models import Emprendedor, User
from app.models.feria_models import Feria


#esto lo uso para el tema de la reseña
from django.core.validators import MinValueValidator, MaxValueValidator


    # TODO: Agregar los siguientes modelos:
    # class Categoria(models.Model): ...  ← extraer categoria a FK
    # class Emprendedor(models.Model): ...
    # class Inscripcion(models.Model): ...


    
  

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
class Resena(models.Model):
    feria = models.ForeignKey(
        Feria,
        on_delete=models.CASCADE
    )

    emprendedor = models.ForeignKey(
        Emprendedor,
        on_delete=models.CASCADE
    )

    comentario = models.TextField()

    puntuacion = models.PositiveIntegerField(
    validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ]
)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("feria", "emprendedor")

    def __str__(self):
        return f"Reseña de {self.emprendedor.nombre}"
    
    @classmethod
    def validate(cls, feria, emprendedor, comentario, puntuacion):
        errors = []

        if not feria:
            errors.append("La feria es obligatoria.")

        if not emprendedor:
            errors.append("El emprendedor es obligatorio.")

        if not comentario or not comentario.strip():
            errors.append("El comentario es obligatorio.")

        if puntuacion is None or puntuacion < 1 or puntuacion > 5:
            errors.append("La puntuación debe estar entre 1 y 5.")

        return errors
    @classmethod
    def new(cls, feria, emprendedor, comentario, puntuacion):
        errors = cls.validate(
            feria,
            emprendedor,
            comentario,
            puntuacion
        )
        if errors:
            return None, errors
        resena = cls.objects.create(
            feria=feria,
            emprendedor=emprendedor,
            comentario=comentario.strip(),
            puntuacion=puntuacion
        )

        return resena, []
    
    def update(self, comentario, puntuacion):
        errors = self.__class__.validate(
            self.feria,
            self.emprendedor,
            comentario,
            puntuacion
        )

        if errors:
            return errors

        self.comentario = comentario.strip()
        self.puntuacion = puntuacion
        self.save()

        return []