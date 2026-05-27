from django.urls import path
from usuarios.views.lista_emprendedores import ListaEmprendedoresView
from usuarios.views.login_view import CustomLoginView
from django.contrib.auth.views import LogoutView

app_name = "usuarios"
urlpatterns = [
    path("emprendedores/", ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]