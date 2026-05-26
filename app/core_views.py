"""Vistas públicas de la aplicación de ferias."""

from django.views.generic import TemplateView
#from django.urls import reverse_lazy

#from app.models.feria_models import Feria
class HomeView(TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "home.html"
   
 
 
# TODO: implementar las siguientes vistas:
# class DetalleFeriaView(DetailView): ...
# class NuevaFeriaView(CreateView): ...
# class ListaEmprendedoresView(ListView): ...
# class NuevaInscripcionView(CreateView): ...
# class CancelarInscripcionView(View): ...
