from django.urls import reverse_lazy
from django.views.generic import CreateView
from usuarios.models.user_models import User
from usuarios.forms.registro_vis_form import RegistroVisitanteForm

class RegistroVisitanteView(CreateView):
    model = User
    form_class = RegistroVisitanteForm
    template_name = "usuarios/registro_vis.html"
    success_url = reverse_lazy("usuarios:login")