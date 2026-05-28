

# Create your models here.


from django.db import models

from django.core.validators import RegexValidator

from usuarios.models.user_models import User


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
    def new(cls, nombre, apellido, rubro, telefono, usuario):
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
        

    def update(self,nombre, apellido, rubro, telefono, usuario ):
        errors = self.__class__.validate(nombre, apellido, rubro, telefono, usuario)
        if errors:
            return errors
        self.nombre=nombre.strip()
        self.apellido=apellido.strip()
        self.rubro=rubro.strip()
        self.telefono=telefono.strip()

        self.save()
        return[]
