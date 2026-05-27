from django.contrib.auth.views import LoginView
from usuarios.forms.login_form import LoginForm
class CustomLoginView(LoginView):

    template_name = "usuarios/login.html"

    authentication_form = LoginForm