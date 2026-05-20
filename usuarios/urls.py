from django.urls import path
from usuarios import views as user_views


app_name = "usuarios"
urlpatterns = [
    path("emprendedores/", user_views.ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
]