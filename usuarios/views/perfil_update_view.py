from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy

class UsuarioUpdateView(LoginRequiredMixin,UpdateView):
    pass