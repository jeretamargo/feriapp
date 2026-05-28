from django.urls import path
from usuarios.views.lista_emprendedores import ListaEmprendedoresView
from usuarios.views.lista_personas import ListaPersonas


app_name = "usuarios"
urlpatterns = [
    path("emprendedores/", ListaEmprendedoresView.as_view(), name="lista_emprendedores"),

    path("personas/", ListaPersonas.as_view(), name="lista_personas"),

]