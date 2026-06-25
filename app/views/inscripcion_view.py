from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.mixins.EmprendedorReq import EmprendedorRequiredMixin
from app.mixins.AdminReq import AdminRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from app.forms.inscripcion_form import InscripcionForm
from usuarios.models.notificacion_models import Notificacion
from app.models.feria_models import Feria
from app.models.inscripcion_models import Inscripcion
from django.contrib import messages

from usuarios.models.user_models import User


class NuevaInscripcionView(EmprendedorRequiredMixin, LoginRequiredMixin, CreateView):


    model = Inscripcion

    template_name = "inscripciones/nueva_inscripcion.html"

    form_class = InscripcionForm

    success_url = reverse_lazy(
        "app:mis_inscripciones"
    )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ferias activas disponibles
        context["ferias"] = Feria.objects.filter(activa=True)

        # ferias en las que el emprendedor ya está inscripto
        if hasattr(self.request.user, "emprendedor"):
            context["ferias_inscripto"] = set(
                Inscripcion.objects.filter(
                    emprendedor=self.request.user.emprendedor
                ).values_list("feria_id", flat=True)
            )
        else:
            context["ferias_inscripto"] = set()

        return context

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
        form.instance.registrado_por = None
        
        

        Notificacion.new(
            usuario=self.request.user,
            asunto="Inscripción realizada",
            mensaje=(
                f"Enviaste correctamente tu inscripcion "
                f"en la feria '{feria.nombre}, en espera de aprobación'."
            ),
            url= reverse("ferias:mis_inscripciones")
        )

        admins = User.objects.filter(is_superuser=True)

        for admin in admins:
            Notificacion.new(
            usuario=admin,
            asunto="Inscripcion Pendiente",
            mensaje=(
                f"Hay una inscripcion pendiente por confirmar, "
                f"Feria '{feria.nombre}, por el usuario {self.request.user.username}'."
            ),
            url= reverse("ferias:solicitudes_inscripciones")
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
            ),
            url= reverse("ferias:mis_inscripciones")
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
    #ver las que esten en "lista_espera"
    def get_queryset(self):
        return Inscripcion.objects.filter(
            estado="lista_espera"
        ).select_related(
            "feria",
            "emprendedor"
        )
    #para ver un historial de las aprobaciones, osea las que no esten en  "lista_espera"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["historial"] = (
            Inscripcion.objects
            .exclude(estado="lista_espera")
            .select_related("feria", "emprendedor")
            .order_by("-id")
        )

        return context
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
        if not inscripcion.feria.tiene_lugar(): #validacion

            messages.error(
                request,
                "La feria ya no tiene puestos disponibles."
            )

            return redirect(
                "app:lista_solicitudes"
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
        inscripcion.registrado_por = request.user  #agregue para que se registre quien lo aprobo      
        inscripcion.save()

        Notificacion.new(
            usuario=inscripcion.emprendedor.usuario,
            asunto="Inscripción aprobada",
            mensaje=(
                f"Tu inscripción a la feria "
                f"'{inscripcion.feria.nombre}' "
                f"fue aprobada. "
                f"Tu puesto asignado es el Nº {puesto}."
            ),
            url=reverse("ferias:mis_inscripciones")
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

        inscripcion.estado = "cancelada"
        inscripcion.registrado_por = request.user
        inscripcion.save()


        Notificacion.new(
            usuario=inscripcion.emprendedor.usuario,
            asunto="Inscripción rechazada",
            mensaje=(
                f"Tu inscripción a la feria "
                f"'{inscripcion.feria.nombre}' "
                f"fue rechazada."
            ),
            url=reverse("ferias:mis_inscripciones")
        )

        messages.warning(
            request,
            "Inscripción rechazada correctamente."
        )

        return redirect(
            "app:solicitudes_inscripciones"
        )