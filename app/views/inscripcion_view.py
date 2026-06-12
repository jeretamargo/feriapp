from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.mixins.EmprendedorReq import EmprendedorRequiredMixin
from app.mixins.AdminReq import AdminRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from app.forms.inscripcion_form import InscripcionForm
from usuarios.models.notificacion_models import Notificacion
from app.models.inscripcion_models import Inscripcion
from django.contrib import messages


class NuevaInscripcionView(EmprendedorRequiredMixin, LoginRequiredMixin, CreateView):


    model = Inscripcion

    template_name = "inscripciones/nueva_inscripcion.html"

    form_class = InscripcionForm

    success_url = reverse_lazy(
        "app:mis_inscripciones"
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



        form.instance.emprendedor = emprendedor
        form.instance.numero_puesto = None
        form.instance.estado = "lista_espera"
        form.instance.registrado_por = self.request.user

        Notificacion.new(
            usuario=self.request.user,
            asunto="Inscripción realizada",
            mensaje=(
                f"Te inscribiste correctamente "
                f"en la feria '{feria.nombre}'."
            )
        )
        messages.success(
            self.request,
            f"Tu solicitud para la feria '{feria.nombre}' fue enviada."
        )
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

class CancelarInscripcionView(EmprendedorRequiredMixin,LoginRequiredMixin,ListView):
    def post(self, request, pk):
        inscripcion = get_object_or_404(
            Inscripcion,
            pk=pk,
            emprendedor=request.user.emprendedor
        )

        # Validacion para que si esta en lista de espera o confimado cancele
        if inscripcion.estado == "cancelada":

            messages.warning(
                request,
                "La inscripción ya estaba cancelada."
            )

            return redirect(
                "app:mis_inscripciones"
            )

        nombre_feria = inscripcion.feria.nombre
        inscripcion.delete()

        Notificacion.new(
            usuario=request.user,
            asunto="Inscripción cancelada",
            mensaje=(
                f"Tu inscripción a la feria "
                f"'{nombre_feria}' "
                f"fue cancelada correctamente."
            )
        )

        messages.success(
            request,
            f"Se canceló tu inscripción a "
            f"'{inscripcion.feria.nombre}'."
        )

        return redirect(
            "app:mis_inscripciones"
        )

class ListaSolicitudesView(AdminRequiredMixin,LoginRequiredMixin, ListView):
    model = Inscripcion

    template_name = "inscripciones/solicitudes.html"

    context_object_name = "solicitudes"

    def get_queryset(self):
        return Inscripcion.objects.filter(
            estado="lista_espera"
        ).select_related(
            "feria",
            "emprendedor"
        )
class AprobarInscripcionView(AdminRequiredMixin,LoginRequiredMixin,ListView):
    def post(self, request, pk):
        inscripcion = get_object_or_404(
            Inscripcion,
            pk=pk
        )
        if inscripcion.estado == "confirmada":
            messages.warning(
                request,
                "La inscripción ya estaba aprobada."
            )
            return redirect(
                "app:inscripciones_pendientes"
            )

        puestos_ocupados = Inscripcion.objects.filter(
            feria=inscripcion.feria,
            estado="confirmada"
        ).values_list(
            "numero_puesto",
            flat=True
        )

        puesto = 1
        while puesto in puestos_ocupados:
            puesto += 1
        
        #valdacion por la moscas
        if Inscripcion.objects.filter( #busca las inscripciones confirmadas 
            feria=inscripcion.feria,
            numero_puesto=puesto,
            estado="confirmada"
        ).exclude(
            pk=inscripcion.pk #Ignora la inscripción actual para no compararla consigo misma
        ).exists():

            messages.error(
                request,
                "Ese puesto ya está ocupado."
            )

            return redirect(
                "app:inscripciones_pendientes"
            )
        inscripcion.numero_puesto = puesto
        inscripcion.estado = "confirmada"        
        inscripcion.save()

        Notificacion.new(
            usuario=inscripcion.emprendedor.usuario,
            asunto="Inscripción aprobada",
            mensaje=(
                f"Tu inscripción a la feria "
                f"'{inscripcion.feria.nombre}' "
                f"fue aprobada. "
                f"Tu puesto asignado es el Nº {puesto}."
            )
        )

        messages.success(
            request,
            "Inscripción aprobada correctamente."
        )

        return redirect(
            "app:solicitudes_inscripciones"
        )
    
class RechazarInscripcionView(AdminRequiredMixin,LoginRequiredMixin,ListView):
    def post(self, request, pk):
        inscripcion = get_object_or_404(
            Inscripcion,
            pk=pk
        )

        if inscripcion.estado == "cancelada":

            messages.warning(
                request,
                "La inscripción ya estaba rechazada."
            )

            return redirect(
                "app:inscripciones_pendientes"
            )

        inscripcion.delete()

        Notificacion.new(
            usuario=inscripcion.emprendedor.usuario,
            asunto="Inscripción rechazada",
            mensaje=(
                f"Tu inscripción a la feria "
                f"'{inscripcion.feria.nombre}' "
                f"fue rechazada."
            )
        )

        messages.warning(
            request,
            "Inscripción rechazada correctamente."
        )

        return redirect(
            "app:solicitudes_inscripciones"
        )