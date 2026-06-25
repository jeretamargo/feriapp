from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from usuarios.forms.login_form import LoginForm
class CustomLoginView(LoginView):

    template_name = "usuarios/login.html"

    authentication_form = LoginForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("ferias:solicitudes_inscripciones") 
        else:
            return reverse_lazy("ferias:home") 