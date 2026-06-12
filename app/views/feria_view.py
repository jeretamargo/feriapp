from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins.AdminReq import AdminRequiredMixin
from app.forms.form_feria import FeriaForm
from app.models.feria_models import Feria
from app.models.categoria_models import Categoria


class ListaFeriasView(LoginRequiredMixin,ListView):
    """Lista todas las ferias activas."""

    model = Feria
    template_name = "ferias/lista_ferias.html"
    context_object_name = "ferias"
    

    def get_queryset(self):
        qs = Feria.objects.all()
        # aplicar filtros desde query params
        if self.request.GET:
            nombre = self.request.GET.get("nombre")
            categoria = self.request.GET.get("categoria")
            fecha_from = self.request.GET.get("fecha_inicio_from")
            fecha_to = self.request.GET.get("fecha_inicio_to")
            ubicacion = self.request.GET.get("ubicacion")
            activa = self.request.GET.get("activa")

            if nombre:
                qs = qs.filter(nombre__icontains=nombre)
            if categoria:
                qs = qs.filter(categoria=categoria)
            if fecha_from:
                qs = qs.filter(fecha_inicio__gte=fecha_from)
            if fecha_to:
                qs = qs.filter(fecha_inicio__lte=fecha_to)
            if ubicacion:
                qs = qs.filter(ubicacion__icontains=ubicacion)
            # Si el parámetro 'activa' vino explícitamente en la query y vale
            # "true" o "false", aplicarlo. Si no viene o viene vacío, no
            # aplicamos filtro (por defecto mostrar todas).
            if 'activa' in self.request.GET:
                if activa == "true":
                    qs = qs.filter(activa=True)
                elif activa == "false":
                    qs = qs.filter(activa=False)
        else:
            # form inválido: no aplicar filtro por defecto (mostrar todas)
            pass

        return qs.order_by("fecha_inicio")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pasar las categorias y ubicaciones para los dropdowns
        context["categorias"] = Categoria.objects.all()
        context["ubicaciones"] = Feria.objects.values_list('ubicacion', flat=True).distinct()
        return context
    
    

class NuevaFeriaView(AdminRequiredMixin,LoginRequiredMixin,CreateView):
    """Vista para crear una nueva feria."""

    model = Feria
    template_name = "ferias/nueva_feria.html"
    form_class = FeriaForm
    #fields = ["nombre", "categoria", "fecha_inicio", "fecha_fin", "ubicacion", "capacidad_puestos"]
    success_url = reverse_lazy('ferias:lista_ferias')
    

    def form_valid(self, form):
        """Marca la feria como activa al crearla."""
        response = super().form_valid(form)
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
        
        messages.info(
        self.request,
        f"La Feria '{self.object.nombre}' fue actualizada correctamente. "
        f"<a href='{reverse_lazy('ferias:detalle_feria', args=[self.object.pk])}' class='alert-link'>Ver detalle</a>")
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Enviar todos los errores del formulario como mensajes
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, f"Error general: {error}")
                else:
                    messages.error(self.request, f"Error en {field}: {error}")
        return super().form_invalid(form)
    