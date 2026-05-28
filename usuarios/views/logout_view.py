from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
class CustomLogoutView(LoginRequiredMixin, LogoutView):

    next_page = "usuarios:login"