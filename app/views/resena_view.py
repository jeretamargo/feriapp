from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from app.models.resena_models import Resena


class ListaResenasView(LoginRequiredMixin, ListView):
    """lista todas las reseñas."""
    model = Resena
    template_name = "usuarios/resenas/lista_resenas.html"
    context_object_name = "resenas"

