# Create your models here.
from django.db import models


from usuarios.models.user_models import User

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
    def new (cls,nombre, apellido, usuario):

        errors = cls.validate(nombre, apellido, usuario)
        if errors:
            return None, errors
        
        visitante = cls.objects.create(
            nombre =nombre,
            apellido=apellido,
            usuario=usuario
        )
        return visitante,[]

        

    
    def update(self,nombre, apellido, usuario):

        errors = self.__class__.validate(nombre, apellido,usuario)
        if errors:
            return errors
        
        self.nombre =nombre.strip()
        self.apellido=apellido.strip()
        self.save()
        return[]