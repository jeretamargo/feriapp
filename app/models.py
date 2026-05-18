"""Modelos de dominio para la aplicación de ferias."""

from __future__ import annotations

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    pass

"""
El modelo User en django ya existe y trae muchas caracteristicas ya implementadas, bajo ningun concepto conviene reinventarlo, por lo que se extiende con AbstractUser para agregarle el campo Notificacion
"""
class Notificacion(models.Model):
    usuario= models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificaciones") #Los "related_name" nos permiten luego poder llamar el campo desde user.notificacion, por ejemplo 
    asunto= models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True) #Guarda automaticamente fecha y hora de creacion

    def marcar_leida(self):
        self.leida=True
        self.save()
    
    @classmethod
    def validate(cls, usuario, asunto, mensaje):
         errors = []

         if not usuario:
            errors.append("No existe usario asignado a la notificación.")

         if not asunto or not asunto.strip() :
            errors.append("El asunto es obligatorio")

         if not mensaje or not mensaje.strip() :
            errors.append("El mensaje es obligatorio")
         return errors

    @classmethod
    def new(cls, usuario, asunto, mensaje):
        errors = cls.validate(usuario, asunto, mensaje)
        if errors:
            return None, errors
        

        notificacion = cls.objects.create(
            usuario=usuario,
            asunto=asunto.strip(),
            mensaje = mensaje.strip()
        )

        return notificacion, []

    
    def update(self, usuario,asunto, mensaje):
        errors = self.__class__.validate(usuario, asunto, mensaje)
        if errors:
            return errors
        
        self.asunto = asunto.strip()
        self.mensaje = mensaje.strip()
        self.save()
        return[]
        


class Emprendedor (models.Model):
    nombre= models.CharField(max_length=200)
    apellido=models.CharField(max_length=200)
    email= models.EmailField(max_length=254, unique=True)
    rubro = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r'^\+?[\d\s\-()]+$',
            message="Ingrese un teléfono válido."
        )
    ])
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="emprendedor")

    """Representacion legible en django admin"""
    def __str__(self):
        return self.nombre
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @classmethod
    def validate(cls, nombre, apellido, email, rubro, telefono, usuario):

        errors=[]

        if not nombre or not nombre.strip():
            errors.append("El nombre es obligatorio")

        if not apellido or not apellido.strip():
            errors.append("El apellido es obligatorio")

        if not email or not email.strip():
            errors.append("El email es obligatorio")

        if not rubro or not rubro.strip():
            errors.append("El rubro es obligatorio") 

        if not telefono or not telefono.strip():
            errors.append("El número de teléfono es obligatorio")

        if not usuario:
            errors.append("El user es obligatorio")

        return errors


    @classmethod
    def new(cls, nombre, apellido, email, rubro, telefono, usuario):
        errors = cls.validate(nombre, apellido, email, rubro, telefono, usuario)
        if errors:
            return None, errors
        
        emprendedor = cls.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=usuario.email, #el mail lo recibe directamente del user
            rubro=rubro,
            telefono=telefono,
            usuario=usuario
        )
        return emprendedor, []
        

    def update(self,nombre, apellido, email, rubro, telefono, usuario ):
        errors = self.__class__.validate(nombre, apellido, email, rubro, telefono, usuario)
        if errors:
            return errors
        self.nombre=nombre.strip()
        self.apellido=apellido.strip()
        self.rubro=rubro.strip()
        self.telefono=telefono.strip()
        #No tiene sentido actualizar ni el email ni el usuario
        self.save()
        return[]

        


class Visitante(models.Model):
    nombre= models.CharField(max_length=200)
    apellido= models.CharField(max_length=200)
    email= models.EmailField(max_length=254, unique=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,related_name="visitante")
    fecha_registro = models.DateField(auto_now_add=True) #Guarda automaticamente fecha de creacion


    """Representacion legible en django admin"""
    def __str__(self):
        return self.nombre
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    @classmethod
    def validate(cls, nombre, apellido, email, usuario):

        errors = []
        if not usuario:
            errors.append("El user es obligatorio")
        if not nombre or not nombre.strip():
            errors.append("El nombre es obligatorio")
        if not apellido or not apellido.strip():
            errors.append("El apellido es obligatorio")

        if not email or not email.strip():
            errors.append("El email es obligatorio")

        return errors

    @classmethod
    def new (cls,nombre, apellido, email, usuario):

        errors = cls.validate(nombre, apellido, email, usuario)
        if errors:
            return None, errors
        
        visitante = cls.objects.create(
            nombre =nombre,
            apellido=apellido,
            email=usuario.email,#El mail lo recibe directamente del user
            usuario=usuario
        )
        return visitante,[]

        

    
    def update(self,nombre, apellido, email, usuario):

        errors = self.__class__.validate(nombre, apellido, email,usuario)
        if errors:
            return errors
        
        self.nombre =nombre.strip()
        self.apellido=apellido.strip()
        #No tiene sentido actualizar ni el email ni el usuario
        self.save()
        return[]
    
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
    
    