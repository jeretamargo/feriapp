from django.urls import reverse_lazy
from django.views.generic import CreateView
from usuarios.models.user_models import User
from usuarios.forms.registro_vis_form import RegistroVisitanteForm
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

from usuarios.models.visitante_models import Visitante

class RegistroVisitanteView(CreateView):
    model = User
    form_class = RegistroVisitanteForm
    template_name = "usuarios/registro_vis.html"
    success_url = reverse_lazy("usuarios:login")

    def form_valid(self, form):

        with transaction.atomic():

            user = form.save(commit=False)
            user.tipo_usuario = "visitante"

            user.save()

            visitante, errores = Visitante.new(
            usuario=user,
            nombre=form.cleaned_data["nombre"],
            apellido=form.cleaned_data["apellido"],)
            if errores:
                for error in errores:
                    form.add_error(None, error)

                raise ValidationError("Error al crear visitante")

            grupo = Group.objects.get(name="Visitante")
            user.groups.add(grupo)

        return super().form_valid(form)
