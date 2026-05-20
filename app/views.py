"""Vistas públicas de la aplicación de ferias."""

from django.views.generic import ListView, TemplateView, CreateView
from django.urls import reverse_lazy

from .models import Feria,Resena


class HomeView(TemplateView):
    """Vista de inicio. Por ahora vacía — completar con estadísticas."""

    template_name = "ferias/home.html"


class ListaFeriasView(ListView):
    """Lista todas las ferias activas."""

    model = Feria
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"

    def get_queryset(self):
        """Retorna solo las ferias marcadas como activas."""
        return Feria.objects.filter(activa=True)


# TODO: implementar las siguientes vistas:
# class DetalleFeriaView(DetailView): ...
# class NuevaFeriaView(CreateView): ...
# class ListaEmprendedoresView(ListView): ...
# class NuevaInscripcionView(CreateView): ...
# class CancelarInscripcionView(View): ...

class NuevaFeriaView(CreateView):
    """Vista para crear una nueva feria."""

    model = Feria
    template_name = "ferias/nueva_feria.html"
    fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos"]
    success_url = reverse_lazy('ferias:lista_ferias')
    

    def form_valid(self, form):
        """Marca la feria como activa al crearla."""
        
        form.instance.activa = True
        
        return super().form_valid(form)

class ListaResenas(ListView):

    model = Resena
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"

    def get_queryset(self):
        """Retorna solo las ferias marcadas como activas."""
        return Feria.objects.filter(activa=True)