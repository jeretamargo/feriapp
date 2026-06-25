from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class EmprendedorOAdminRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.groups.filter(name="Emprendedor").exists() or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(
            self.request,
            "No tenés permisos para acceder a esta sección."
        )
        return redirect("/")