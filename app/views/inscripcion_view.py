from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.mixins.EmprendedorReq import EmprendedorRequiredMixin

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from app.forms.inscripcion_form import InscripcionForm
from usuarios.models.notificacion_models import Notificacion
from app.models.inscripcion_models import Inscripcion
from django.contrib import messages


class NuevaInscripcionView(EmprendedorRequiredMixin, LoginRequiredMixin, CreateView):


    model = Inscripcion

    template_name = "inscripciones/nueva_inscripcion.html"

    form_class = InscripcionForm

    success_url = reverse_lazy(
        "app:home"
    )

    def form_valid(self, form):
        #en caso que un visitante entra aca, para que no explote agrego esta verificacion
        if not hasattr(self.request.user, "emprendedor"):
            form.add_error(
                None,
                "Solo los emprendedores pueden inscribirse."
            )
            return self.form_invalid(form)
        
        emprendedor = self.request.user.emprendedor
        feria = form.instance.feria

        #para q no le deje inscribirse en la misma feria dos veces
        if Inscripcion.objects.filter(
            feria=form.instance.feria,
            emprendedor=self.request.user.emprendedor
        ).exists():

            form.add_error(
                "feria",
                "Ya estás inscripto en esta feria."
            )
            return self.form_invalid(form)
        
        if not feria.tiene_lugar():
            form.add_error(
                "feria",
                "No hay puestos disponibles."
            )
            return self.form_invalid(form)

        puestos_ocupados = Inscripcion.objects.filter(
            feria=feria
        ).exclude(
            estado="cancelada"
        ).values_list("numero_puesto", flat=True)

        puesto = 1

        while puesto in puestos_ocupados:
            puesto += 1

        form.instance.emprendedor = emprendedor
        form.instance.numero_puesto = puesto
        form.instance.estado = "confirmada"
        form.instance.registrado_por = self.request.user

        Notificacion.new(
            usuario=self.request.user,
            asunto="Inscripción realizada",
            mensaje=(
                f"Te inscribiste correctamente "
                f"en la feria '{feria.nombre}'."
            ),
            url= reverse("ferias:mis_inscripciones")
        )
        messages.success(
            self.request,
            f"Te inscribiste correctamente en la feria '{feria.nombre}'.")

        return super().form_valid(form)
    

class MisInscripcionesView(EmprendedorRequiredMixin, LoginRequiredMixin,ListView):
    model = Inscripcion

    template_name = "inscripciones/mis_inscripciones.html"

    context_object_name = "inscripciones"

    def get_queryset(self):
        if not hasattr(
            self.request.user,
            "emprendedor"
        ):
            return Inscripcion.objects.none()

        return Inscripcion.objects.filter(
            emprendedor=self.request.user.emprendedor
        ).select_related("feria")


    #vista para cancelar inscripcion
def cancelar_inscripcion(request, pk):
        if request.method != "POST":
            return redirect("app:mis_inscripciones")
        #el get_object_or_404 es para que un emprendedor no puede cancelar la inscripción de otro emprendedor
        inscripcion = get_object_or_404(
            Inscripcion,
            pk=pk,
            emprendedor=request.user.emprendedor
        )

        inscripcion.estado = "cancelada"
        inscripcion.save()

        Notificacion.new(
            usuario=request.user,
            asunto="Inscripción cancelada",
            mensaje=(
                f"Tu inscripción a la feria "
                f"'{inscripcion.feria.nombre}' "
                f"fue cancelada correctamente."
            ),
            url= reverse("ferias:mis_inscripciones")
        )
        messages.success(
            request,
            f"Se canceló tu inscripción a '{inscripcion.feria.nombre}'."
            )
        return redirect("app:mis_inscripciones")