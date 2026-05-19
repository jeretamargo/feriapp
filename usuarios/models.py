from django.db import models

# Create your models here.
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
    rubro = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r'^\+?[\d\s\-()]+$',
            message="Ingrese un teléfono válido." #Un teléfono puede tener múltiples  patrones que incluyen espacios y signos, por eso se le asigna charfield (y no integer) y se valida con una expresión regular
        )
    ])
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="emprendedor")

    """Representacion legible en django admin"""
    def __str__(self):
        return self.nombre
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @classmethod
    def validate(cls, nombre, apellido, rubro, telefono, usuario):

        errors=[]

        if not nombre or not nombre.strip():
            errors.append("El nombre es obligatorio")

        if not apellido or not apellido.strip():
            errors.append("El apellido es obligatorio")

        if not rubro or not rubro.strip():
            errors.append("El rubro es obligatorio") 

        if not telefono or not telefono.strip():
            errors.append("El número de teléfono es obligatorio")

        if not usuario:
            errors.append("El user es obligatorio")

        return errors


    @classmethod
    def new(cls, nombre, apellido, email, rubro, telefono, usuario):
        errors = cls.validate(nombre, apellido, rubro, telefono, usuario)
        if errors:
            return None, errors
        
        emprendedor = cls.objects.create(
            nombre=nombre,
            apellido=apellido,
            rubro=rubro,
            telefono=telefono,
            usuario=usuario
        )
        return emprendedor, []
        

    def update(self,nombre, apellido, email, rubro, telefono, usuario ):
        errors = self.__class__.validate(nombre, apellido, rubro, telefono, usuario)
        if errors:
            return errors
        self.nombre=nombre.strip()
        self.apellido=apellido.strip()
        self.rubro=rubro.strip()
        self.telefono=telefono.strip()

        self.save()
        return[]

        


class Visitante(models.Model):
    nombre= models.CharField(max_length=200)
    apellido= models.CharField(max_length=200)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,related_name="visitante")
    fecha_registro = models.DateField(auto_now_add=True) #Guarda automaticamente fecha de creacion


    """Representacion legible en django admin"""
    def __str__(self):
        return self.nombre
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    @classmethod
    def validate(cls, nombre, apellido, usuario):

        errors = []
        if not usuario:
            errors.append("El user es obligatorio")
        if not nombre or not nombre.strip():
            errors.append("El nombre es obligatorio")
        if not apellido or not apellido.strip():
            errors.append("El apellido es obligatorio")

        

        return errors

    @classmethod
    def new (cls,nombre, apellido, email, usuario):

        errors = cls.validate(nombre, apellido, usuario)
        if errors:
            return None, errors
        
        visitante = cls.objects.create(
            nombre =nombre,
            apellido=apellido,
            usuario=usuario
        )
        return visitante,[]

        

    
    def update(self,nombre, apellido, email, usuario):

        errors = self.__class__.validate(nombre, apellido,usuario)
        if errors:
            return errors
        
        self.nombre =nombre.strip()
        self.apellido=apellido.strip()
        self.save()
        return[]