from django.views.generic import TemplateView
class UsuarioPerfilView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["es_emprendedor"] = self.request.user.groups.filter(
            name="Emprendedor"
        ).exists()

        context["es_visitante"] = self.request.user.groups.filter(
            name="Visitante"
        ).exists()

        return context
    template_name = "usuarios/perfil.html"