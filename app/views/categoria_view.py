from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from app.forms.categoria_form import CategoriaForm
from app.models.categoria_models import Categoria
from django.contrib import messages
from django.shortcuts import redirect
from app.mixins.AdminReq import AdminRequiredMixin
from django.http import HttpResponseRedirect
from app.mixins.EmprendedorOAdminReq import EmprendedorOAdminRequiredMixin


class ListaCategoriaView(EmprendedorOAdminRequiredMixin, LoginRequiredMixin,ListView):
    """Lista todas las Categorias activas."""

    model = Categoria
    template_name = "categorias/lista_categorias.html"
    context_object_name = "categorias"

class NuevaCategoriaView(AdminRequiredMixin, LoginRequiredMixin,CreateView):
    """Formulario para crear una nueva categoría."""
    model = Categoria
    form_class = CategoriaForm
    template_name = "categorias/nueva_categoria.html"
    success_url = reverse_lazy("app:lista_categorias")
    
    def form_valid(self, form):
        """Marca la categoría como activa al crearla."""
        data = form.cleaned_data
        categoria, errors = Categoria.new(data.get("nombre"), data.get("descripcion"))
        if errors:
            for err in errors:
                messages.error(self.request, err)
            return self.form_invalid(form)

        self.object = categoria
        messages.success(self.request, f"La categoría '{self.object.nombre}' fue creada exitosamente.")
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
    

class UpdateCategoriaView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    """Vista para actualizar una categoría."""
    model = Categoria
    form_class = CategoriaForm
    template_name = "categorias/actualizar_categoria.html"
    success_url = reverse_lazy("app:lista_categorias")
    
    def form_valid(self, form):
        data = form.cleaned_data
        errors = self.object.update(data.get("nombre"), data.get("descripcion"))
        if errors:
            for err in errors:
                messages.error(self.request, err)
            return self.form_invalid(form)

        messages.info(self.request, f"La categoría '{self.object.nombre}' fue actualizada correctamente.")
        return HttpResponseRedirect(self.get_success_url())
    
    

class DeleteCategoriaView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    """Vista para eliminar una categoría."""

    model = Categoria
    template_name = "categorias/confirmar_borrado.html"
    success_url = reverse_lazy("app:lista_categorias")
    

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Verificar si tiene ferias asociadas
        if self.object.ferias.exists():
            messages.error(request, "No se puede borrar la categoría porque tiene ferias asociadas.")
            return redirect(self.success_url)
        else:
            return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        # Agregar mensaje de éxito después de borrar la categoría, de otra manera no muestra el mensaje. (solo delete)
        messages.warning(self.request, f"La categoría '{self.object.nombre}' fue borrada exitosamente.")
        return super().get_success_url()
        
    #TODO arreglar la vista de messages.
    


