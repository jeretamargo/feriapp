
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from usuarios.forms.password_update_form import PasswordUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

class PasswordUpdateView(LoginRequiredMixin,PasswordChangeView):
    form_class = PasswordUpdateForm
    template_name = "usuarios/editar_password.html"
    success_url = reverse_lazy("usuarios:login")
    def form_valid(self, form):
        messages.success(
            self.request,
            "La contraseña fue actualizada correctamente."
        )
        return super().form_valid(form)
    
