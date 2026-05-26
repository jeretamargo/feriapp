from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

from app.forms.categoria_form import CategoriaForm
from app.models.categoria_models import Categoria


class ListaCategoriaView(ListView):
    """Lista todas las Categorias activas."""

    model = Categoria
    template_name = "categorias/lista_categorias.html"
    context_object_name = "categorias"

class NuevaCategoriaView(CreateView):
    """Formulario para crear una nueva categoría."""

    model = Categoria
    form_class = CategoriaForm
    template_name = "categorias/nueva_categoria.html"
    success_url = reverse_lazy("app:lista_categorias")

class DeleteCategoriaView(DeleteView):
    """Vista para eliminar una categoría."""

    model = Categoria
    template_name = "categorias/confirmar_borrado.html"
    success_url = reverse_lazy("app:lista_categorias")

class UpdateCategoriaView(UpdateView):
    """Vista para actualizar una categoría."""

    model = Categoria
    form_class = CategoriaForm
    template_name = "categorias/actualizar_categoria.html"
    success_url = reverse_lazy("app:lista_categorias")
    
    


