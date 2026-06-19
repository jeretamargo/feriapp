from django.urls import reverse_lazy
from django.views.generic import CreateView
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User
from usuarios.forms.registro_emp_form import RegistroEmprendedorForm
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group




class RegistroEmprendedorView(CreateView):
    model = User
    form_class = RegistroEmprendedorForm
    template_name = "usuarios/registro_emp.html"
    success_url = reverse_lazy("usuarios:login")

    def form_valid(self, form):

        with transaction.atomic():

            user = form.save(commit=False)
            user.tipo_usuario = "emprendedor"

            user.save()

            emprendedor, errores = Emprendedor.new(
                usuario=user,
                nombre=form.cleaned_data["nombre"],
                apellido=form.cleaned_data["apellido"],
                rubro=form.cleaned_data["rubro"],
                telefono=form.cleaned_data["telefono"],
            )

            if errores:
                for error in errores:
                    form.add_error(None, error)

                raise ValidationError("Error al crear emprendedor")

            grupo = Group.objects.get(name="Emprendedor")
            user.groups.add(grupo)

        return super().form_valid(form)