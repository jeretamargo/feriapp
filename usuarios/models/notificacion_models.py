from django.db import models

from user_models import User


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
        
