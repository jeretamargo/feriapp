from django.urls import reverse_lazy
from django.views.generic import CreateView
from usuarios.models.user_models import User
from usuarios.forms.registro_emp_form import RegistroEmprendedorForm

class RegistroEmprendedorView(CreateView):
    model = User
    form_class = RegistroEmprendedorForm
    template_name = "usuarios/registro.html"
    success_url = reverse_lazy("usuarios:login")