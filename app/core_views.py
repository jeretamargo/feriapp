"""Vistas públicas de la aplicación de ferias."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Avg, Count
from django.db import models

from app.models.feria_models import Feria
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.visitante_models import Visitante
#from django.urls import reverse_lazy

#from app.models.feria_models import Feria
class HomeView(LoginRequiredMixin, TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """Agrega la cantidad de puestos ocupados y disponibles a la plantilla."""
        context = super().get_context_data(**kwargs)
        context["nro_ferias_totales"] = Feria.objects.filter().count()
        context["nro_ferias_activas"] = Feria.objects.filter(activa=True).count()
        context["nro_emprendedores"] = Emprendedor.objects.all().count()
        context["nro_visitantes"] = Visitante.objects.all().count()
        context["ferias_activas"] = Feria.objects.filter(activa=True)
        context["emprendedor_destacado"] = (
            Emprendedor.objects
            .annotate( # esto agrega campos calculados a cada objeto del queryset sin guardarlos en la base de datos
                promedio=Avg("resena__puntuacion"), #promedio con la puntuacion de las resenas dividiendo la cantidad osea (5 + 4 + 5) / 3
                cantidad_resenas=Count("resena") #cuantas resenas tiene los emprendedor
            )
            .filter(cantidad_resenas__gt=0)#solo los que tengan mas de 0 resenas
            .order_by("-promedio")#mejor solo traigo a uno
            .first()
            #.order_by("-promedio")[:3] #ordeno de mayor a menor y muestro los 3 mejores
        )

        context["feria_destacada"] = (
            Feria.objects
            .annotate(#cuenta los emprendedores distintos con inscripción confirmada por feria, ordena de mayor a menor y toma el primero
                total_emprendedores=Count("inscripcion__emprendedor", distinct=True, filter=models.Q(inscripcion__estado="confirmada"))
            )
            .filter(total_emprendedores__gt=0)
            .order_by("-total_emprendedores")
            .first()
        )

        return context
 
