from __future__ import annotations

from django.db import models
from .feria_models import Feria
from django.utils import timezone



class Sector(models.Model):
    """Representa un sector de actividad para los emprendedores."""

    nombre = models.CharField(max_length=100, unique=True)
    edicion = models.DateField(blank=True, null=True)
    capacidad_puestos = models.PositiveIntegerField()
    tiene_conexion_electrica = models.BooleanField(default=False)
    feria = models.ForeignKey(Feria, on_delete=models.CASCADE, related_name="sectores")

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        unique_together = ["feria", "nombre"] # evita duplicados dentro de la misma feria
        
    def es_edicion_actual(self):
        """Retorna True si la edición del sector coincide con el año actual."""
        return self.edicion.year == timezone.now().year

    
    def descripcion_completa(self):
        """Retorna una descripción completa del sector."""
        conexion = "con conexión eléctrica" if self.tiene_conexion_electrica else "sin conexión eléctrica"
        return f"{self.nombre} (Edición: {self.edicion}, Capacidad: {self.capacidad_puestos} puestos, {conexion})"
    
    
    def validate(self) -> list[str]:
        errors = []
        if not self.nombre or not self.nombre.strip():
            errors.append("El nombre del sector es obligatorio.")
        if len(self.nombre.strip()) < 3:
            errors.append("El nombre del sector debe tener al menos 3 caracteres.")
        if self.capacidad_puestos <= 0:
            errors.append("La capacidad de puestos debe ser mayor a cero.")

        return errors
    
    def update(self, nombre, edicion, capacidad_puestos, tiene_conexion_electrica) -> list[str]:
        """Actualiza los datos del sector si son válidos. Retorna una lista de errores."""
        self.nombre = nombre.strip()
        self.edicion = edicion
        self.capacidad_puestos = capacidad_puestos
        self.tiene_conexion_electrica = tiene_conexion_electrica
        errors = self.validate()
        if errors:
            return errors
        self.save()
        return []

    @classmethod
    def new(cls, nombre, edicion, capacidad_puestos, tiene_conexion_electrica) -> tuple[Sector | None, list[str]]:
        """Crea y persiste un nuevo sector si los datos son válidos. Retorna (instancia, errors)."""
        sector = cls(nombre=nombre.strip(), edicion=edicion, capacidad_puestos=capacidad_puestos, tiene_conexion_electrica=tiene_conexion_electrica)
        errors = sector.validate()
        if errors:
            return None, errors
        sector.save()
        return sector, []
  