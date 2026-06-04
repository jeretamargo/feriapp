from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Inscripcion
from app.mixins.EmprendedorReq import EmprendedorRequiredMixin


class NuevaInscripcionView(EmprendedorRequiredMixin, LoginRequiredMixin, CreateView):
    """Vista para crear una nueva inscripción."""

    model= Inscripcion
    template_name = "ferias/nueva_inscripcion.html"
    fields = ["feria", "numero_puesto",  "estado"]
