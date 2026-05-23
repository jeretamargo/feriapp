"""Vistas públicas de la aplicación de ferias."""

from django.views.generic import TemplateView, CreateView
#from django.urls import reverse_lazy

#from app.models.feria_models import Feria
from .core_models import Inscripcion



class HomeView(TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "ferias/home.html"

class NuevaInscripcionView(CreateView):
    """Vista para crear una nueva inscripción."""

    model= Inscripcion
    template_name = "ferias/nueva_inscripcion.html"
    fields = ["feria", "numero_puesto",  "estado"]


# TODO: implementar las siguientes vistas:
# class DetalleFeriaView(DetailView): ...
# class NuevaFeriaView(CreateView): ...
# class ListaEmprendedoresView(ListView): ...
# class NuevaInscripcionView(CreateView): ...
# class CancelarInscripcionView(View): ...
