"""Compatibilidad: re-exportar modelos dispersos en varios módulos.

Este __init__ permite seguir usando `from app.models import Feria, Categoria, ...`
durante la reestructuración.
"""

from .categoria_models import Categoria
from .feria_models import Feria
from .sector_models import Sector

# Inscripcion vive en app/core_models.py (mantener nombre disponible)
from .inscripcion_models import Inscripcion
from .resena_models import Resena
# Emprendedor estaba en el módulo de usuarios; lo exponemos aquí
# para mantener compatibilidad con imports existentes en tests.
from usuarios.models.emprendedor_models import Emprendedor

# Exponer explícitamente los nombres que queremos que estén disponibles al importar desde este módulo
# permite importar con from app.models import Clase.
__all__ = [
	"Categoria",
	"Feria",
	"Sector",
	"Inscripcion",
	"Emprendedor",
    "Resena",  
]
