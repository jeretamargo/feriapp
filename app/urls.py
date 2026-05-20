"""Definición de rutas públicas de la aplicación."""

from django.urls import path
from . import views
from usuarios import views as user_views

app_name = "app"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ferias/", views.ListaFeriasView.as_view(), name="lista_ferias"),
    path('emprendedores/lista', user_views.ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
    path("ferias/nueva/", views.NuevaFeriaView.as_view(), name="nueva_feria")
    ]
    
    
    # TODO:
    # path("ferias/<int:pk>/", views.DetalleFeriaView.as_view(), name="detalle_feria"),
    # path("emprendedores/", views.ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
    # path("inscripciones/nueva/", views.NuevaInscripcionView.as_view(), name="nueva_inscripcion"),

<<<<<<< HEAD
=======
    path("resena/", views..as_view(), name="nueva_feria"),

    path("resena/nueva/", views..as_view(), name="nueva_feria"),

]
>>>>>>> 6c56d3c670f5103d7fe9b9c22eb7b367758be142
