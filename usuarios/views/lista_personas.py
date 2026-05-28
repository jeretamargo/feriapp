from django.views.generic import ListView

from usuarios.models.visitante_models import Visitante
# Create your views here.
class ListaPersonas(ListView):
    """Lista todas las ferias activas."""
    model=Visitante
    template_name = "usuarios/templates/lista_personas.html"
    context_object_name = "personas"
