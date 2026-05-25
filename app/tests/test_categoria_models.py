from datetime import date

from django.test import TestCase
from django.db import IntegrityError

from app.models.categoria_models import Categoria
from app.models.feria_models import Feria
from app.models.sector_models import Sector
from usuarios.models import Emprendedor, User
from app.models import Inscripcion, Resena


class CategoriaModelTest(TestCase):
    """Tests para el modelo Categoria."""

    def setUp(self):
        Categoria.objects.create(nombre="Artesanías")
        Categoria.objects.create(nombre="Tecnología")

    def test_str_retorna_nombre(self):
        categoria = Categoria.objects.get(nombre="Artesanías")
        self.assertEqual(str(categoria), "Artesanías")

    def test_contar_ferias_retorna_cantidad_correcta(self):
        categoria = Categoria.objects.get(nombre="Artesanías")
        Feria.objects.create(
            nombre="Feria X",
            categoria=categoria,
            fecha_inicio=date(2026, 6, 1),
            fecha_fin=date(2026, 6, 2),
            ubicacion="Lugar",
            capacidad_puestos=5,
        )
        self.assertEqual(categoria.contar_ferias(), 1)

    def test_is_categoria_activa_true_y_false(self):
        categoria = Categoria.objects.get(nombre="Tecnología")
        # sin ferias activas
        self.assertFalse(categoria.is_categoria_activa())
        # agregar feria activa
        Feria.objects.create(
            nombre="Feria Tech",
            categoria=categoria,
            fecha_inicio=date(2026, 8, 1),
            fecha_fin=date(2026, 8, 2),
            ubicacion="Centro",
            capacidad_puestos=10,
            activa=True,
        )
        self.assertTrue(categoria.is_categoria_activa())

    def test_lista_ferias_retorna_lista(self):
        categoria = Categoria.objects.get(nombre="Artesanías")
        Feria.objects.create(
            nombre="Feria A",
            categoria=categoria,
            fecha_inicio=date(2026, 5, 1),
            fecha_fin=date(2026, 5, 2),
            ubicacion="Plaza",
            capacidad_puestos=8,
        )
        lista = categoria.lista_ferias()
        self.assertIsInstance(lista, list)
        self.assertTrue(all(isinstance(f, Feria) for f in lista))

    #carga completa, sin errores
    def test_validate_datos_correctos_retorna_lista_vacia(self):
        categoria = Categoria(nombre="Valida", descripcion="Desc")
        errors = categoria.validate()
        self.assertEqual(errors, [])

    # nombre vacio
    def test_validate_nombre_vacio_retorna_error(self):
        categoria = Categoria(nombre="", descripcion="")
        errors = categoria.validate()
        self.assertTrue(len(errors) > 0)

    # nombre corto
    def test_validate_nombre_corto_retorna_error(self):
        categoria = Categoria(nombre="ab", descripcion="")
        errors = categoria.validate()
        self.assertTrue(len(errors) > 0)

    # count antes aumenta, cuando se crea la categoria
    def test_new_crea_categoria_con_datos_validos(self):
        count_antes = Categoria.objects.count()
        categoria, errors = Categoria.new("Diseño", "Descripción")
        self.assertEqual(errors, [])
        self.assertIsNotNone(categoria)
        self.assertEqual(Categoria.objects.count(), count_antes + 1)

    # count antes no cambia, no se crea la categoria
    def test_new_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Categoria.objects.count()
        categoria, errors = Categoria.new("", "")
        self.assertIsNone(categoria)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Categoria.objects.count(), count_antes)

    # cambio de nombre, sin errores
    def test_update_modifica_datos_correctamente(self):
        categoria = Categoria.objects.create(nombre="Antes", descripcion="X")
        errors = categoria.update("Después", "Nueva desc")
        self.assertEqual(errors, [])
        categoria.refresh_from_db()
        self.assertEqual(categoria.nombre, "Después")

    # update datos erroneos, no se modifica
    def test_update_con_datos_invalidos_no_modifica(self):
        categoria = Categoria.objects.create(nombre="Original", descripcion="X")
        errors = categoria.update("", "")
        self.assertTrue(len(errors) > 0)
        categoria.refresh_from_db()
        self.assertEqual(categoria.nombre, "Original")

