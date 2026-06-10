from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from app.mixins.AdminReq import AdminRequiredMixin
from app.models import Sector
from app.forms.sector_form import SectorForm
from django.http import HttpResponseRedirect


# List View 
class SectorListView( LoginRequiredMixin, ListView):
    model = Sector
    template_name = 'sectores/lista_sector.html'
    context_object_name = 'sectores'
    #paginate_by = 10


# Detail View 
class SectorDetailView(AdminRequiredMixin,LoginRequiredMixin, DetailView):
    model = Sector
    template_name = 'sectores/detalle_sector.html'
    context_object_name = 'sector'
    
    def getcontext_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sector = self.get_object()
        context['descripcion_completa'] = sector.descripcion_completa()
        return context
    
    


# Create View 
class SectorCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Sector
    template_name = 'sectores/nuevo_sector.html'
    #fields = '__all__'
    success_url = reverse_lazy('ferias:lista_sector')
    form_class = SectorForm
    
    def form_valid(self, form):
        """Agrega mensajes de éxito o error al crear un sector."""
        data = form.cleaned_data
        sector, errors = Sector.new(
            data.get("nombre"),
            data.get("edicion"),
            data.get("capacidad_puestos"),
            data.get("tiene_conexion_electrica"),
            data.get("feria"),
        )
        if errors:
            for err in errors:
                messages.error(self.request, err)
            return self.form_invalid(form)

        self.object = sector
        messages.success(self.request, f"El sector '{self.object.nombre}' fue creado correctamente."
                         f" <a href='{reverse_lazy('ferias:detalle_sector', args=[self.object.pk])}' class='alert-link'>Ver detalle</a>")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """Agrega mensajes de error al intentar crear un sector con datos inválidos."""
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, f"Error general: {error}")
                else:
                    messages.error(self.request, f"Error en {field}: {error}")
        return super().form_invalid(form)
    

# Update View 
class SectorUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Sector
    template_name = 'sectores/actualizar_sector.html'
    #fields = '__all__'
    form_class = SectorForm
    success_url = reverse_lazy('ferias:lista_sector')
    
    def form_valid(self, form):
        """Agrega mensajes de éxito o error al actualizar un sector."""
        data = form.cleaned_data
        errors = self.object.update(
            data.get("nombre"),
            data.get("edicion"),
            data.get("capacidad_puestos"),
            data.get("tiene_conexion_electrica"),
            data.get("feria"),
        )
        if errors:
            for err in errors:
                messages.error(self.request, err)
            return self.form_invalid(form)

        messages.success(self.request, f"El sector '{self.object.nombre}' fue actualizado correctamente."
                         f" <a href='{reverse_lazy('ferias:detalle_sector', args=[self.object.pk])}' class='alert-link'>Ver detalle</a>")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """Agrega mensajes de error al intentar actualizar un sector con datos inválidos."""
        for field, errors in form.errors.items():
            for error in errors:
                if field == "__all__":
                    messages.error(self.request, f"Error general: {error}")
                else:
                    messages.error(self.request, f"Error en {field}: {error}")
        return super().form_invalid(form)
    


# Delete View  
class SectorDeleteView(AdminRequiredMixin,LoginRequiredMixin, DeleteView):
    model = Sector
    template_name = 'sectores/borrar_sector.html'
    success_url = reverse_lazy('ferias:lista_sector')
    
    def get_success_url(self):
        messages.warning(self.request, f"El sector '{self.object.nombre}' fue borrado exitosamente.")
        return super().get_success_url()
    
