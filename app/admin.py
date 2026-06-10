"""Configuración del panel de administración para la app principal."""

from django.contrib import admin
from app.models.sector_models import Sector
from app.models.feria_models import Feria
from app.models.categoria_models import Categoria
from app.models.inscripcion_models import Inscripcion
from app.models.resena_models import Resena


# TODO: reemplazar por @admin.register con list_display, list_filter, search_fields


@admin.register(Feria)
class FeriaAdmin(admin.ModelAdmin):
    pass

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    pass

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    pass

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    pass