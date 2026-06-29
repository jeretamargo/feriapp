from __future__ import annotations

from django.db import models

from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User
from app.models.feria_models import Feria


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
    #cambio aca para que me deje ponerlo en estado de lista_espera y que este en none hasta q el admin lo acepte
    numero_puesto = models.PositiveIntegerField( null=True, blank=True)

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
    #para que cada empprendedor solo pueda estar inscripto una vez en la feria
    class Meta:
        unique_together = [
        ("feria", "emprendedor"),
        #cambie la logica para solamente no te permita inscribir un emprendedor dos veces en la misma feria
    ]

    def __str__(self):
        return f"{self.emprendedor} - {self.feria}"

    @classmethod
    def validate(cls, feria, emprendedor, numero_puesto, estado):
        errors = []
        #verifica si el puesto ya está ocupado cuando se crea una inscripción nueva
        if feria and cls.objects.filter(
            feria=feria,
            numero_puesto=numero_puesto,
            estado="confirmada"
            ).exists():
            errors.append(
                "El puesto ya está ocupado."
        )
        

        if not feria:
            errors.append("La feria es obligatoria.")

        if not emprendedor:
            errors.append("El emprendedor es obligatorio.")

        #cambie el validate porq una inscripcion en espera no tiene puesto
        if (
            estado == "confirmada"
            and
            (
                numero_puesto is None
                or
                numero_puesto <= 0
            )
        ):
            errors.append(
                "El número de puesto debe ser mayor a cero."
            )

        estados_validos = [e[0] for e in cls.ESTADOS]

        if estado not in estados_validos:
            errors.append("Estado inválido.")
        #para validar si la feria tiene espacio y ademas estar validado
        if feria and estado == "confirmada" and not feria.tiene_lugar():
            errors.append("La feria no tiene puestos disponibles.")

        return errors
    
    @classmethod
    #añadi para que se guarde quien lo registro
    def new(cls, feria, emprendedor, estado="confirmada", registrado_por=None):
        #calcula el primer puesto libre y se le asigna al emprendedor
        puestos_ocupados = cls.objects.filter(
            feria=feria
        ).values_list(
            "numero_puesto",
            flat=True
        )
        numero_puesto = 1
        while numero_puesto in puestos_ocupados:
            numero_puesto += 1

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
            estado=estado, 
            registrado_por=registrado_por,
        )

        return inscripcion, []
    
    def update(self, numero_puesto, estado):
            # esto es para verificar si el puesto no estaba siendo ocupado por otra persona o emprendedor
        if self.__class__.objects.filter(
            feria=self.feria,
            numero_puesto=numero_puesto
        ).exclude(pk=self.pk).exists():
            return ["El puesto ya está ocupado en esta feria."]
        
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