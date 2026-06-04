from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class VisitanteRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.groups.filter(name="Visitantes").exists()

    def handle_no_permission(self):
        messages.error(
            self.request,
            "No tenés permisos para acceder a esta sección."
        )
        return redirect("/")