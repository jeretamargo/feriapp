"""Definición de rutas públicas de la aplicación."""

from django.urls import path
from app.views import  feria_view, categoria_view, sector_view,inscripcion_view,resena_view #, sector_view
from .core_views import HomeView

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
    
    path("sectores/", sector_view.SectorListView.as_view(), name="lista_sector"),
    path("sectores/nueva/", sector_view.SectorCreateView.as_view(), name="nuevo_sector"),
    path("sectores/<int:pk>/actualizar/", sector_view.SectorUpdateView.as_view(), name="actualizar_sector"),
    path("sectores/<int:pk>/borrar/", sector_view.SectorDeleteView.as_view(), name="borrar_sector"),
    path("sectores/<int:pk>/", sector_view.SectorDetailView.as_view(), name="detalle_sector"),
    
    path("inscripciones/nueva/", inscripcion_view.NuevaInscripcionView.as_view(), name="nueva_inscripcion"),

    path("mis-inscripciones/", inscripcion_view.MisInscripcionesView.as_view(), name="mis_inscripciones"),
    
    path("inscripciones/<int:pk>/cancelar/",inscripcion_view.CancelarInscripcionView.as_view(),name="cancelar_inscripcion"),  
      
    path("inscripciones/solicitudes/",inscripcion_view.ListaSolicitudesView.as_view(),name="solicitudes_inscripciones"),
    path("inscripciones/<int:pk>/aprobar/",inscripcion_view.AprobarInscripcionView.as_view(),name="aprobar_inscripcion"),
    path("inscripciones/<int:pk>/rechazar/",inscripcion_view.RechazarInscripcionView.as_view(),name="rechazar_inscripcion"),



    path("resenas/todas/", resena_view.ListadeTodasResenasView.as_view(),name="lista_completa_de_resenas"),

    path("resenas/", resena_view.ListaResenasView.as_view(),name="lista_resenas"),
    
    path("resenas/nueva/", resena_view.NuevaResenaView.as_view(),name="nueva_resena"),

    ##emprendedor vea sus resenas que le hicieron
    path("resenas/mis-resenas/", resena_view.MisResenasView.as_view(), name="mis_resenas"),

    ]
    
    
    # TODO:
    # path("ferias/<int:pk>/", views.DetalleFeriaView.as_view(), name="detalle_feria"),
    # path("emprendedores/", views.ListaEmprendedoresView.as_view(), name="lista_emprendedores"),
    # path("inscripciones/nueva/", views.NuevaInscripcionView.as_view(), name="nueva_inscripcion"),

    #   path("resena/", views.ListaResenas.as_view(), name="lista_reseñas"),
    #   path("resena/nueva/", views..as_view(), name="nueva_feria"),  

    