"""Definición de rutas públicas de la aplicación."""

from django.urls import path
from app.views import  feria_view, categoria_view #, sector_view
from .core_views import HomeView
from .views.resena_view import ListaResenasView
from .views.inscripcion_view import NuevaInscripcionView,MisInscripcionesView,cancelar_inscripcion

#from usuarios import views as user_views

app_name = "app"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    path("ferias/", feria_view.ListaFeriasView.as_view(), name="lista_ferias"),
    path("ferias/nueva/", feria_view.NuevaFeriaView.as_view(), name="nueva_feria"),
    path('ferias/<int:pk>/', feria_view.DetalleFeriaView.as_view(), name="detalle_feria"),
    path("ferias/<int:pk>/borrar/", feria_view.DeleteFeriaView.as_view(), name="borrar_feria"),
    path("ferias/<int:pk>/actualizar/", feria_view.UpdateFeriaView.as_view(), name="actualizar_feria"),
    
    path("categorias/", categoria_view.ListaCategoriaView.as_view(), name="lista_categorias"),
    path("categorias/nueva/", categoria_view.NuevaCategoriaView.as_view(), name="nueva_categoria"),
    path("categorias/<int:pk>/actualizar/", categoria_view.UpdateCategoriaView.as_view(), name="actualizar_categoria"),
    path("categorias/<int:pk>/borrar/", categoria_view.DeleteCategoriaView.as_view(), name="borrar_categoria"),
    
    path("inscripciones/nueva/", NuevaInscripcionView.as_view(), name="nueva_inscripcion"),

    path("mis-inscripciones/", MisInscripcionesView.as_view(), name="mis_inscripciones"),
    
    path("inscripciones/<int:pk>/cancelar/",cancelar_inscripcion,name="cancelar_inscripcion"),

    path("resenas/", ListaResenasView.as_view(),name="lista_resenas"),
    
    
    ]
    
    
    # TODO:
    # path("ferias/<int:pk>/", views.DetalleFeriaView.as_view(), name="detalle_feria"),
    # path("emprendedores/", views.ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
    # path("inscripciones/nueva/", views.NuevaInscripcionView.as_view(), name="nueva_inscripcion"),

    #   path("resena/", views.ListaResenas.as_view(), name="lista_reseñas"),
    #   path("resena/nueva/", views..as_view(), name="nueva_feria"),  

    