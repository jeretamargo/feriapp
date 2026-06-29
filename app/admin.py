"""Configuración del panel de administración para la app principal."""

from django.contrib import admin
from app.models.sector_models import Sector
from app.models.feria_models import Feria
from app.models.categoria_models import Categoria
from app.models.inscripcion_models import Inscripcion
from app.models.resena_models import Resena
from app.forms.feria_admin_form import FeriaAdminForm
from app.forms.inscripcion_admin_form import InscripcionAdminForm

# TODO: reemplazar por @admin.register con list_display, list_filter, search_fields

class SectorInline(admin.TabularInline):
    model = Sector
    extra = 0

class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0

class FeriaInline(admin.TabularInline):
    model = Feria
    extra = 0

@admin.register(Feria)
class FeriaAdmin(admin.ModelAdmin):
    # Columnas a mostrar en la tabla principal
 list_display = ('nombre', 'categoria', 'fecha_inicio', 'fecha_fin', 'capacidad_puestos', 'ubicacion', 'activa')
 form=FeriaAdminForm
 autocomplete_fields = ("categoria",)
 # Panel lateral derecho para filtrar por fecha o instructor
 list_filter = ('fecha_inicio', 'categoria', 'capacidad_puestos', 'ubicacion')

 # Barra de búsqueda superior (busca por título de curso o nombre de instructor)
 # Nota: Como instructor es ForeignKey, usamos la sintaxis de doble guion bajo
 search_field = ('nombre')
 # Paginación (cuántos ítems por página)
 list_per_page = 10

 fieldsets = (
 ('Información Principal', {
 'fields': ('nombre', 'categoria', 'ubicacion')
 }),
 ('Caracteristicas', {
 'fields': ('fecha_inicio', 'fecha_fin', 'capacidad_puestos', 'activa')
 }),
 )
 inlines = [InscripcionInline, SectorInline]
    

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin): 
    list_display = ('nombre', 'edicion', 'capacidad_puestos', 'tiene_conexion_electrica', 'feria')

  
    list_filter = ('nombre', 'capacidad_puestos', 'tiene_conexion_electrica', 'feria')

    
    search_fields = ('nombre', 'edicion')
    
    list_per_page = 10

    

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
     
     list_display = ('nombre', 'descripcion' )

  
     list_filter = ('nombre', 'descripcion')

    
     search_fields = ('nombre', 'descripcion')
   
     list_per_page = 10

     inlines=[FeriaInline]

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):

    form=InscripcionAdminForm

    list_display = ('emprendedor', 'feria', 'numero_puesto', 'fecha_inscripcion', 'estado', 'registrado_por' )

  
    list_filter = ('emprendedor__nombre', 'estado','fecha_inscripcion', 'feria__nombre' )

    
    search_fields = ('emprendedor__nombre', 'emprendedor__apellido', 'feria__nombre')
   
    list_per_page = 10


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('emprendedor', 'visitante', 'comentario', 'puntuacion' )

  
    list_filter = ('emprendedor__nombre', 'visitante__nombre','emprendedor__apellido', 'visitante__apellido', 'puntuacion'  )

    
    search_fields = ('emprendedor__nombre', 'visitante__nombre','emprendedor__apellido', 'visitante__apellido', 'puntuacion')
   
    list_per_page = 10
    