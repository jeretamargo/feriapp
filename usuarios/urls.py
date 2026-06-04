from django.urls import path
from usuarios.views.lista_emprendedores import ListaEmprendedoresView
from usuarios.views.login_view import CustomLoginView
from usuarios.views.logout_view import CustomLogoutView
from usuarios.views.password_update_view import PasswordUpdateView
from usuarios.views.perfil_view import UsuarioPerfilView
from usuarios.views.registro_emp_view import RegistroEmprendedorView
from usuarios.views.registro_vis_view import RegistroVisitanteView
from usuarios.views.registro_eleccion_view import RegistroEleccionView

app_name = "usuarios"
urlpatterns = [
    path("emprendedores/", ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/emprendedor/', RegistroEmprendedorView.as_view(), name='registro_emprendedor'),
    path('registro/visitante/', RegistroVisitanteView.as_view(), name='registro_visitante'),
    path('registro/', RegistroEleccionView.as_view(), name='registro'),
    path('perfil/', UsuarioPerfilView.as_view(), name='perfil'),
    path('perfil/editar/password/', PasswordUpdateView.as_view(), name='editar_password'),
]