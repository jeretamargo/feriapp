from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Inscripcion
from django.urls import reverse_lazy



class NuevaInscripcionView(LoginRequiredMixin,CreateView):
    """Vista para crear una nueva inscripción."""

    model= Inscripcion
    template_name = "ferias/nueva_inscripcion.html"
    fields = ["emprendedor","feria", "numero_puesto",  "estado"]
    success_url = reverse_lazy(
        #"app:lista_inscripciones"
    )