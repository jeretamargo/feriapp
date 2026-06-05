"""Configuración del panel de administración para la app principal."""

from django.contrib import admin
from app.models.sector_models import Sector
from app.models.feria_models import Feria
from app.models.categoria_models import Categoria
from app.models.inscripcion_models import Inscripcion
from app.models.resena_models import Resena


# TODO: reemplazar por @admin.register con list_display, list_filter, search_fields
admin.site.register(Feria)
admin.site.register(Sector)
admin.site.register(Categoria)
admin.site.register(Inscripcion)
admin.site.register(Resena)