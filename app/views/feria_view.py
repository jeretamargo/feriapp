from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins.AdminReq import AdminRequiredMixin
from app.forms.form_feria import FeriaForm
from app.models.feria_models import Feria
from django.http import HttpResponseRedirect


class ListaFeriasView(LoginRequiredMixin,ListView):
    """Lista todas las ferias activas."""

    model = Feria
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"

    def get_queryset(self):
        """Retorna solo las ferias marcadas como activas."""
        return Feria.objects.filter(activa=True)
    
    

class NuevaFeriaView(AdminRequiredMixin,LoginRequiredMixin,CreateView):
    """Vista para crear una nueva feria."""

    model = Feria
    template_name = "ferias/nueva_feria.html"
    form_class = FeriaForm
    #fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos"]
    success_url = reverse_lazy('ferias:lista_ferias')
    

    def form_valid(self, form):
        # Usar el método `Feria.new` para crear la instancia usando cleaned_data
        data = form.cleaned_data
        feria, errors = Feria.new(
            data.get("nombre"),
            data.get("categoria"),
            data.get("fecha_inicio"),
            data.get("fecha_fin"),
            data.get("ubicacion"),
            data.get("capacidad_puestos"),
        )
        if errors:
            for err in errors:
                messages.error(self.request, err)
            return self.form_invalid(form)

        self.object = feria
        response = HttpResponseRedirect(self.get_success_url())
        # if not self.request.user.has_perm("ferias.add_feria"):
        #     messages.error(self.request, "No tienes permisos para crear ferias.")
        #     return self.form_invalid(form)
        
        messages.success(
        self.request,
        f"La Feria '{self.object.nombre}' fue creada correctamente. "
        f"<a href='{reverse_lazy('ferias:detalle_feria', args=[self.object.pk])}' class='alert-link'>Ver detalle</a>")
        
        return response
    
    def form_invalid(self, form):
        # Enviar todos los errores del formulario como mensajes
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, f"Error general: {error}")
                else:
                    messages.error(self.request, f"Error en {field}: {error}")
        return super().form_invalid(form)

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
    
class DeleteFeriaView(AdminRequiredMixin,LoginRequiredMixin,DeleteView):
    """Vista para eliminar una feria."""

    model = Feria
    template_name = "ferias/borrar_feria.html"
    success_url = reverse_lazy('ferias:lista_ferias')
    
    def get_success_url(self):
        messages.warning(self.request, f"La feria '{self.object.nombre}' fue borrada exitosamente.")
        return super().get_success_url()

class UpdateFeriaView(AdminRequiredMixin,LoginRequiredMixin,UpdateView):
    """Vista para actualizar una feria."""

    model = Feria
    form_class = FeriaForm
    template_name = "ferias/actualizar_feria.html"
    #fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos"]
    success_url = reverse_lazy('ferias:lista_ferias')
    
    def form_valid(self, form):
        """Marca la feria como activa al actualizarla."""
        data = form.cleaned_data
        errors = self.object.update(
            data.get("nombre"),
            data.get("categoria"),
            data.get("fecha_inicio"),
            data.get("fecha_fin"),
            data.get("ubicacion"),
            data.get("capacidad_puestos"),
        )
        if errors:
            for err in errors:
                messages.error(self.request, err)
            return self.form_invalid(form)

        messages.info(
            self.request,
            f"La Feria '{self.object.nombre}' fue actualizada correctamente. "
            f"<a href='{reverse_lazy('ferias:detalle_feria', args=[self.object.pk])}' class='alert-link'>Ver detalle</a>")
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        # Enviar todos los errores del formulario como mensajes
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, f"Error general: {error}")
                else:
                    messages.error(self.request, f"Error en {field}: {error}")
        return super().form_invalid(form)
    