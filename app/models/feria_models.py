"""Modelos de dominio para la aplicación de ferias."""

from __future__ import annotations

from django.db import models
from django.db.models import Sum

from .categoria_models import Categoria


#esto lo uso para el tema de la reseña
from django.core.validators import MinValueValidator, MaxValueValidator

class Feria(models.Model):
    """Representa una feria con su período, ubicación y capacidad disponible."""

    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey("Categoria", on_delete=models.PROTECT, related_name="ferias")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ubicacion = models.CharField(max_length=200)
    capacidad_puestos = models.PositiveIntegerField()
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["fecha_inicio"]

    def __str__(self):
        """Retorna una representación legible de la feria."""
        return self.nombre

    def puestos_ocupados(self):
        """Retorna la cantidad de inscripciones confirmadas."""
        # Mientras Inscripcion no exista, no hay relaciones para contar.
        if not hasattr(self, "inscripcion_set"):
            return 0
        return self.inscripcion_set.filter(estado="confirmada").count()

    def puestos_disponibles(self):
        """Retorna los puestos libres."""
        return self.capacidad_puestos - self.puestos_ocupados()

    def capacidad_ocupada_por_sectores(self, sector_actual=None):
        """Retorna la capacidad total de puestos ya asignada a los sectores de esta feria.

        Si se proporciona sector_actual, su capacidad no se incluye en la suma.
        Esto permite validar actualizaciones sin contar doble la misma instancia.
        """
        sectores = self.sectores.all()
        if sector_actual is not None and hasattr(sector_actual, "pk"):
            sectores = sectores.exclude(pk=sector_actual.pk)
        total = sectores.aggregate(total=Sum("capacidad_puestos"))["total"]
        return total or 0

    def capacidad_disponible_para_sectores(self, sector_actual=None):
        """Retorna la capacidad restante disponible para un sector nuevo o actualizado."""
        return self.capacidad_puestos - self.capacidad_ocupada_por_sectores(sector_actual=sector_actual)

    def hay_lugar_para_sector(self, capacidad_nueva, sector_actual=None):
        """Retorna True si esta feria admite un sector con la capacidad solicitada.

        sector_actual se usa solo para actualizar un sector existente, de modo que
        no se contabilice su capacidad anterior dos veces.
        """
        if capacidad_nueva is None or capacidad_nueva <= 0:
            return False
        return self.capacidad_disponible_para_sectores(sector_actual=sector_actual) >= capacidad_nueva

    def capacidad_minima_por_sectores(self):
        """Retorna la capacidad mínima que debe tener la feria según los sectores existentes."""
        return self.capacidad_ocupada_por_sectores()

    def tiene_lugar(self):
        """Retorna True si quedan puestos disponibles."""
        return self.puestos_disponibles() > 0
    
    def is_activa(self):
        """Retorna True si la feria está activa."""
        return self.activa
    
    def duracion_dias(self):
        """Retorna la duración de la feria en días."""
        return (self.fecha_fin - self.fecha_inicio).days + 1
    

    @classmethod
    def validate(
        cls, nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
    ):
        """
        Valida los datos de la feria. Retorna una lista de errores.
        Si la lista está vacía, los datos son válidos.
        """
        errors = []

        if not nombre or not nombre.strip():
            errors.append("El nombre es obligatorio.")
        
        if categoria is None or not isinstance(categoria, Categoria):
            errors.append("La categoría debe ser una instancia de Categoria.")
            
        if not ubicacion or not ubicacion.strip():
            errors.append("La ubicación es obligatoria.")

        if capacidad_puestos is None or capacidad_puestos <= 0:
            errors.append("La capacidad de puestos debe ser mayor a cero.")

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            errors.append("La fecha de fin no puede ser anterior a la fecha de inicio.")

        return errors

    @classmethod
    def new(
        cls, nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
    ):
        """
        Crea y persiste una nueva feria si los datos son válidos.
        Retorna (instancia, errors). Si hay errores, instancia es None.
        """
        errors = cls.validate(
            nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
        )
        if errors:
            return None, errors

        feria = cls.objects.create(
            nombre=nombre.strip(),
            categoria=categoria,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            ubicacion=ubicacion.strip(),
            capacidad_puestos=capacidad_puestos,
        )
        return feria, []

    def update(
        self, nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
    ):
        """
        Actualiza los datos de la feria si los datos son válidos.
        Retorna una lista de errores. Si está vacía, la actualización fue exitosa.
        """
        errors = self.__class__.validate(
            nombre, categoria, fecha_inicio, fecha_fin, ubicacion, capacidad_puestos
        )
        if capacidad_puestos is not None:
            capacidad_minima = self.capacidad_minima_por_sectores()
            if capacidad_puestos < capacidad_minima:
                errors.append(
                    f"La capacidad de la feria no puede ser menor que la suma de la capacidad de los sectores existentes ({capacidad_minima} puestos)."
                )
        if errors:
            return errors

        self.nombre = nombre.strip()
        self.categoria = categoria
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.ubicacion = ubicacion.strip()
        self.capacidad_puestos = capacidad_puestos
        self.save()
        return []
