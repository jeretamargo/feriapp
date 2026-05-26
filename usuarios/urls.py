from django.urls import path
from usuarios.views.lista_emprendedores import ListaEmprendedoresView


app_name = "usuarios"
urlpatterns = [
    path("emprendedores/", ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
]