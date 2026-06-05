from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from usuarios.forms.edit_perfil_emp_form import EmprendedorUpdateForm
from usuarios.forms.edit_perfil_vis_form import VisitanteUpdateForm
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.visitante_models import Visitante
from django.shortcuts import redirect
from django.contrib import messages
class PerfilUpdateView(LoginRequiredMixin, UpdateView):

    def get_form_class(self):

        if self.request.user.es_emprendedor():
            return EmprendedorUpdateForm
        elif self.request.user.es_visitante():
            return VisitanteUpdateForm

    def get_object(self):

        if self.request.user.es_emprendedor():
            return self.request.user.emprendedor
        elif self.request.user.es_visitante():
            return self.request.user.visitante
        
    def form_valid(self, form):

        obj = self.get_object()

        if self.request.user.es_emprendedor():

            errors = obj.update(
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                rubro=form.cleaned_data["rubro"],
                telefono=form.cleaned_data["telefono"],
                usuario=obj.usuario,
            )

        elif self.request.user.es_visitante():

            errors = obj.update(
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                usuario=obj.usuario,
            )
        if errors:
            form.add_error(None, errors)
            return self.form_invalid(form)
        messages.success(
            self.request,
            "Sus datos fueron actualizados correctamente."
        )
        return redirect("usuarios:perfil")
        
   
            

        
    template_name="usuarios/editar_perfil.html"