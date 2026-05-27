"""Modelos de dominio para la aplicación de ferias."""

from __future__ import annotations

from django.db import models

from usuarios.models import Emprendedor, User, Visitante
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

    # TODO: Agregar los siguientes modelos:
    # class Categoria(models.Model): ...  ← extraer categoria a FK
    # class Emprendedor(models.Model): ...
    # class Inscripcion(models.Model): ...

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
    
class Sector(models.Model):
    """Representa un sector de actividad para los emprendedores."""

    nombre = models.CharField(max_length=100, unique=True)
    edicion = models.DateField()
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
        from django.utils import timezone
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

        if not visitante:
            errors.append("El visitante es obligatorio.")

        if not emprendedor:
            errors.append("El emprendedor es obligatorio.")

        if not comentario or not comentario.strip():
            errors.append("El comentario es obligatorio.")

        if puntuacion is None or puntuacion < 1 or puntuacion > 5:
            errors.append("La puntuación debe estar entre 1 y 5.")

        return errors
    @classmethod
    def new(cls, visitante, emprendedor, comentario, puntuacion):
        errors = cls.validate(
            visitante,
            emprendedor,
            comentario,
            puntuacion
        )
        if errors:
            return None, errors
        resena = cls.objects.create(
            visitante=visitante,
            emprendedor=emprendedor,
            comentario=comentario.strip(),
            puntuacion=puntuacion
        )

        return resena, []
    
    def update(self, comentario, puntuacion):
        errors = self.__class__.validate(
            self.visitante,
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