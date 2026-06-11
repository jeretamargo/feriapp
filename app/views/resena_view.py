from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins.VisitanteReq import VisitanteRequiredMixin
from app.mixins.AdminReq import AdminRequiredMixin
from app.models.resena_models import Resena
from django.contrib import messages

class ListadeTodasResenasView(AdminRequiredMixin,LoginRequiredMixin, ListView):
    """lista todas las reseñas."""
    model = Resena
    template_name = "resenas/lista_completa_de_resenas.html"
    context_object_name = "resenas"


##la vista basica
class NuevaResenaView(VisitanteRequiredMixin,LoginRequiredMixin,CreateView):

    model = Resena

    template_name = "resenas/nueva_resena.html"

    fields = [
        "emprendedor",
        "comentario",
        "puntuacion"
    ]

    success_url = reverse_lazy(
        "app:lista_resenas"
    )
####

##aca es para tomar el visitante qu esta logueado 
    def form_valid(self, form):

        visitante = self.request.user.visitante

        #aca es para evitar un error cuando intenta resenar al mismo emprendedor y lanza la excepcion
        if Resena.objects.filter(
            visitante=visitante,
            emprendedor=form.instance.emprendedor
        ).exists():

            form.add_error(
                "emprendedor",
                "Ya realizaste una reseña para este emprendedor."
            )

            return self.form_invalid(form)
###
        form.instance.visitante = visitante

        messages.success(
            self.request,
            "Resena creada correctamente."
        )

        return super().form_valid(form)
    
class ListaResenasView(
    VisitanteRequiredMixin,
    LoginRequiredMixin,
    ListView
):
    model = Resena

    template_name = "resenas/lista_resenas.html"

    context_object_name = "resenas"
        #sol vea sus resenas el visitante
    def get_queryset(self):

        return Resena.objects.filter(
            visitante=self.request.user.visitante
        ).select_related(
            "emprendedor"
        )