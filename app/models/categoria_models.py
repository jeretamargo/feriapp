
from __future__ import annotations

from django.db import models



class Categoria(models.Model):
    """Representa una categoría de feria."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)


    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
      
      
    def contar_ferias(self):
        """Retorna la cantidad de ferias asociadas a esta categoría."""
        return self.ferias.count() # el related_name en el FK de Feria es "ferias"
    
    def is_categoria_activa(self):
        """Retorna True si la categoría tiene al menos una feria activa."""
        return self.ferias.filter(activa=True).exists() 
    
    def lista_ferias(self):
        """Retorna una lista de las ferias asociadas a esta categoría."""
        return list(self.ferias.all()) 
    
        
    
    
    def validate(self) -> list[str]:
        errors = []
        if not self.nombre or not self.nombre.strip():
            errors.append("El nombre de la categoría es obligatorio.")
        if len(self.nombre.strip()) < 3:
            errors.append("El nombre debe tener al menos 3 caracteres.")
        return errors
    
    def update(self, nombre, descripcion) -> list[str]:
        """Actualiza los datos de la categoría si son válidos. Retorna una lista de errores."""
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        errors = self.validate()
        if errors:
            return errors
        self.save()
        return []

    @classmethod
    def new(cls, nombre, descripcion) -> tuple[Categoria | None, list[str]]:
        """Crea y persiste una nueva categoría si los datos son válidos. Retorna (instancia, errors)."""
        categoria = cls(nombre=nombre.strip(), descripcion=descripcion.strip()) 
        errors = categoria.validate()
        if errors:
            return None, errors
        categoria.save()
        return categoria, []