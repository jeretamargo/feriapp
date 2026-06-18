from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins.VisitanteReq import VisitanteRequiredMixin
from app.mixins.AdminReq import AdminRequiredMixin
from app.models.resena_models import Resena
from django.contrib import messages
from usuarios.models.emprendedor_models import Emprendedor
from app.forms.resenas_form import ResenaForm
from app.models.inscripcion_models import Inscripcion
from app.models.feria_models import Feria
class ListadeTodasResenasView(AdminRequiredMixin,LoginRequiredMixin, ListView):
    """lista todas las reseñas."""
    model = Resena
    template_name = "resenas/lista_completa_de_resenas.html"
    context_object_name = "resenas"


##la vista basica
class NuevaResenaView(VisitanteRequiredMixin,LoginRequiredMixin,CreateView):

    model = Resena

    template_name = "resenas/nueva_resena.html"

    form_class = ResenaForm

    success_url = reverse_lazy(
        "app:lista_resenas"
    )
####
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["ferias"] = Feria.objects.filter(
            activa=True
        )

        return context
    
    def get_form(self, form_class=None):

            form = super().get_form(form_class)

            feria_id = self.request.GET.get("feria")

            if feria_id:
                form.initial["feria"] = feria_id
                form.fields["emprendedor"].queryset = (
                    Emprendedor.objects.filter(
                        inscripcion__feria_id=feria_id,
                        #para solo ver a los emprendedores confirmados
                        inscripcion__estado="confirmada"

                    ).distinct()
                )

            else:

                form.fields["emprendedor"].queryset = (
                    Emprendedor.objects.none()
                )

            return form

##aca es para tomar el visitante qu esta logueado 
    def form_valid(self, form):

        visitante = self.request.user.visitante
        feria_id = self.request.GET.get("feria")
        if feria_id:

            pertenece = Inscripcion.objects.filter(
                feria_id=feria_id,
                emprendedor=form.instance.emprendedor,
                estado="confirmada"
            ).exists()

            if not pertenece:

                form.add_error(
                    "emprendedor",
                    "El emprendedor no pertenece a esa feria."
                )

                return self.form_invalid(form)
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