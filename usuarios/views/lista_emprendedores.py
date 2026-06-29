from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from usuarios.models.emprendedor_models import Emprendedor
# Create your views here.
class ListaEmprendedoresView(LoginRequiredMixin,ListView):
    """Lista todas las ferias activas."""

    model = Emprendedor
    template_name = "usuarios/templates/usuarios/lista_emprendedores.html"
    context_object_name = "emprendedores"

    #def get_queryset(self):
     #   """Retorna solo las ferias marcadas como activas."""
     #   return Feria.objects.filter(activa=True)