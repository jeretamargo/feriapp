from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from app.forms.form_feria import FeriaForm
from app.models.feria_models import Feria


class ListaFeriasView(LoginRequiredMixin,ListView):
    """Lista todas las ferias activas."""

    model = Feria
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"

    def get_queryset(self):
        """Retorna solo las ferias marcadas como activas."""
        return Feria.objects.filter(activa=True)

class NuevaFeriaView(LoginRequiredMixin,CreateView):
    """Vista para crear una nueva feria."""

    model = Feria
    template_name = "ferias/nueva_feria.html"
    form_class = FeriaForm
    #fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos"]
    success_url = reverse_lazy('ferias:lista_ferias')
    

    def form_valid(self, form):
        """Marca la feria como activa al crearla."""
        
        form.instance.activa = True
        
        return super().form_valid(form)

class DetalleFeriaView(LoginRequiredMixin, DetailView):
    """Vista para mostrar los detalles de una feria."""

    model = Feria
    template_name = "ferias/detalle_feria.html"
    context_object_name = "feria"

    def get_context_data(self, **kwargs):
        """Agrega la cantidad de puestos ocupados y disponibles a la plantilla."""
        context = super().get_context_data(**kwargs)
        context["puestos_ocupados"] = self.object.puestos_ocupados() # pyright: ignore[reportAttributeAccessIssue]
        context["puestos_disponibles"] = self.object.puestos_disponibles() # pyright: ignore[reportAttributeAccessIssue]
        return context
    
class DeleteFeriaView(LoginRequiredMixin,DeleteView):
    """Vista para eliminar una feria."""

    model = Feria
    template_name = "ferias/borrar_feria.html"
    success_url = reverse_lazy('ferias:lista_ferias')

class UpdateFeriaView(LoginRequiredMixin,UpdateView):
    """Vista para actualizar una feria."""

    model = Feria
    form_class = FeriaForm
    template_name = "ferias/actualizar_feria.html"
    #fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos"]
    success_url = reverse_lazy('ferias:lista_ferias')