from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from app.mixins.VisitanteReq import VisitanteRequiredMixin
from app.mixins.AdminReq import AdminRequiredMixin
from app.mixins.EmprendedorReq import EmprendedorRequiredMixin
from app.models.resena_models import Resena
from django.contrib import messages
from usuarios.models.emprendedor_models import Emprendedor
from app.forms.resenas_form import ResenaForm
from app.models.inscripcion_models import Inscripcion
from app.models.feria_models import Feria


class ListadeTodasResenasView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    model = Resena
    template_name = "resenas/lista_completa_de_resenas.html"
    context_object_name = "resenas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Estructura: {feria: {emprendedor: [resenas]}}
        datos = {}

        resenas = Resena.objects.select_related(
            "emprendedor",
            "visitante"
        ).order_by(
            "emprendedor__nombre"
        )

        for resena in resenas:
            # buscar en qué ferias estuvo este emprendedor
            inscripciones = Inscripcion.objects.filter(
                emprendedor=resena.emprendedor,
                estado="confirmada"
            ).select_related("feria")

            for inscripcion in inscripciones:
                feria = inscripcion.feria
                emp = resena.emprendedor

                if feria not in datos:
                    datos[feria] = {}

                if emp not in datos[feria]:
                    datos[feria][emp] = []

                if resena not in datos[feria][emp]:
                    datos[feria][emp].append(resena)

        context["datos"] = datos
        return context

##la vista basica
class NuevaResenaView(VisitanteRequiredMixin, LoginRequiredMixin, CreateView):

    model = Resena
    template_name = "resenas/nueva_resena.html"
    form_class = ResenaForm
    success_url = reverse_lazy("app:lista_resenas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feria_id = self.request.GET.get("feria")
        emprendedor_id = self.request.GET.get("emprendedor")

        #primero dejo ver las feria activas y con almenos un emprendedor
        context["ferias"] = Feria.objects.filter(
            activa=True,
            inscripcion__estado="confirmada"
        ).distinct()

        # si elijo alguna feria muestro los  emprendedores de esa feria
        if feria_id:
            context["feria_seleccionada"] = Feria.objects.filter(pk=feria_id).first()
            context["emprendedores"] = Emprendedor.objects.filter(
                inscripcion__feria_id=feria_id,
                inscripcion__estado="confirmada"
            ).distinct()
        # IDs de emprendedores que el visitante ya reseñó
        if hasattr(self.request.user, "visitante"):
            context["ya_resenados"] = set(
                Resena.objects.filter(
                    visitante=self.request.user.visitante
                ).values_list("emprendedor_id", flat=True)
            )
        else:
            context["ya_resenados"] = set()
            
        # si elijo algun emprendedor pasar el emprendedor seleccionado
        if emprendedor_id:
            context["emprendedor_seleccionado"] = Emprendedor.objects.filter(
                pk=emprendedor_id
            ).first()

        return context

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # guardamos feria_id y emprendedor_id para usarlos en get_form
        self._feria_id = self.request.GET.get("feria")
        self._emprendedor_id = self.request.GET.get("emprendedor")
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        feria_id = getattr(self, '_feria_id', None)
        emprendedor_id = getattr(self, '_emprendedor_id', None)

        if feria_id and emprendedor_id:
            form.fields["emprendedor"].queryset = Emprendedor.objects.filter(
                pk=emprendedor_id,
                inscripcion__feria_id=feria_id,
                inscripcion__estado="confirmada"
            ).distinct()
        else:
            form.fields["emprendedor"].queryset = Emprendedor.objects.none()

        return form
    

    def form_valid(self, form):

        visitante = self.request.user.visitante

        if Resena.objects.filter(
            visitante=visitante,
            emprendedor=form.instance.emprendedor
        ).exists():
            form.add_error(
                "emprendedor",
                "Ya realizaste una reseña para este emprendedor."
            )
            return self.form_invalid(form)

        form.instance.visitante = visitante
        messages.success(self.request, "Reseña creada correctamente.")
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)
    
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
    
class MisResenasView(EmprendedorRequiredMixin, LoginRequiredMixin, ListView):
    model = Resena
    template_name = "resenas/mis_resenas.html"
    context_object_name = "resenas"

    def get_queryset(self):
        emprendedor = self.request.user.emprendedor
        qs = Resena.objects.filter(
            emprendedor=emprendedor
        ).select_related("visitante", "emprendedor")

        # filtro por feria si viene en GET
        feria_id = self.request.GET.get("feria")
        if feria_id:
            qs = qs.filter(
                emprendedor__inscripcion__feria_id=feria_id,
                emprendedor__inscripcion__estado="confirmada"
            ).distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ferias en las que el emprendedor participó confirmado
        context["ferias"] = Feria.objects.filter(
            inscripcion__emprendedor=self.request.user.emprendedor,
            inscripcion__estado="confirmada"
        ).distinct()

        context["feria_seleccionada"] = self.request.GET.get("feria", "")
        return context