from __future__ import annotations

from django.db import models

from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.visitante_models import Visitante



#esto lo uso para el tema de la reseña
from django.core.validators import MinValueValidator, MaxValueValidator

class Resena(models.Model):
   
    emprendedor = models.ForeignKey(
        Emprendedor,
        on_delete=models.CASCADE
    )
    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.CASCADE,
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
        unique_together = ("visitante", "emprendedor")

    def __str__(self):
        return f"Reseña de {self.emprendedor.nombre}"
    
    @classmethod
    def validate(cls, visitante , emprendedor, comentario, puntuacion):
        errors = []

        if not visitante :
            errors.append("El visitante es obligatoria.")

        if not emprendedor:
            errors.append("El emprendedor es obligatorio.")

        if not comentario or not comentario.strip():
            errors.append("El comentario es obligatorio.")

        if puntuacion is None or puntuacion < 1 or puntuacion > 5:
            errors.append("La puntuación debe estar entre 1 y 5.")

        return errors
    @classmethod
    def new(cls, visitante , emprendedor, comentario, puntuacion):
        errors = cls.validate(
            visitante ,
            emprendedor,
            comentario,
            puntuacion
        )
        if errors:
            return None, errors
        resena = cls.objects.create(
            visitante =visitante ,
            emprendedor=emprendedor,
            comentario=comentario.strip(),
            puntuacion=puntuacion
        )

        return resena, []
    
    def update(self, comentario, puntuacion):
        errors = self.__class__.validate(
            self.visitante ,
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