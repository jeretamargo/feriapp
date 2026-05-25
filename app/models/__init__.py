"""Compatibilidad: re-exportar modelos dispersos en varios módulos.

Este __init__ permite seguir usando `from app.models import Feria, Categoria, ...`
durante la reestructuración.
"""

from .categoria_models import Categoria
from .feria_models import Feria
from .sector_models import Sector

# Inscripcion vive en app/core_models.py (mantener nombre disponible)
from ..core_models import Inscripcion

# Emprendedor estaba en el módulo de usuarios; lo exponemos aquí
# para mantener compatibilidad con imports existentes en tests.
from usuarios.models import Emprendedor

__all__ = [
	"Categoria",
	"Feria",
	"Sector",
	"Inscripcion",
	"Emprendedor",
]
