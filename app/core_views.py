"""Vistas públicas de la aplicación de ferias."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

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
        return context
 
