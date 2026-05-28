"""Tests de comportamiento para el modelo Feria."""

from datetime import date

from django.test import TestCase

from app.models.categoria_models import Categoria
from app.models.feria_models import Feria
from app.models.inscripcion_models import Inscripcion
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User
class FeriaModelTest(TestCase):
    """Verifica validaciones y operaciones básicas del modelo Feria."""

    def setUp(self):
        """Crea una feria base reutilizable para cada caso de prueba."""
        # Crear las categorías necesarias para los tests (usar solo `get` en los asserts)
        Categoria.objects.create(nombre="Artesanías")
        Categoria.objects.create(nombre="Tecnología")
        Categoria.objects.create(nombre="Categoría")
        categoria = Categoria.objects.get(nombre="Artesanías")
        self.feria = Feria.objects.create(
            nombre="Feria de Invierno",
            categoria=categoria,
            fecha_inicio=date(2026, 7, 1),
            fecha_fin=date(2026, 7, 3),
            ubicacion="Plaza Central",
            capacidad_puestos=10,
        )

    # --- __str__ y métodos simples ---

    def test_str_retorna_nombre(self):
        self.assertEqual(str(self.feria), "Feria de Invierno")

    def test_activa_por_defecto(self):
        self.assertTrue(self.feria.activa)

    def test_puestos_disponibles_igual_a_capacidad_sin_inscripciones(self):
        self.assertEqual(self.feria.puestos_disponibles(), 10)

    def test_tiene_lugar_true_con_capacidad_libre(self):
        self.assertTrue(self.feria.tiene_lugar())

    # --- validate ---

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        categoria = Categoria.objects.get(nombre="Tecnología")
        errors = Feria.validate(
            "Tech Patagonia",
            categoria,
            date(2026, 9, 1),
            date(2026, 9, 3),
            "Centro Cultural",
            20,
        )
        self.assertEqual(errors, [])

    def test_validate_nombre_vacio_retorna_error(self):
        categoria = Categoria.objects.get(nombre="Tecnología")
        errors = Feria.validate(
            "",
            categoria,
            date(2026, 9, 1),
            date(2026, 9, 3),
            "Centro Cultural",
            20,
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_fecha_fin_anterior_a_inicio_retorna_error(self):
        categoria = Categoria.objects.get(nombre="Categoría")
        errors = Feria.validate(
            "Feria",
            categoria,
            date(2026, 9, 10),
            date(2026, 9, 5),  # fin < inicio
            "Ubicación",
            10,
        )
        self.assertTrue(len(errors) > 0)

    def test_validate_capacidad_cero_retorna_error(self):
        categoria = Categoria.objects.get(nombre="Categoría")
        errors = Feria.validate(
            "Feria",
            categoria,
            date(2026, 9, 1),
            date(2026, 9, 3),
            "Ubicación",
            0,
        )
        self.assertTrue(len(errors) > 0)

    # --- new ---

    def test_new_crea_feria_con_datos_validos(self):
        categoria = Categoria.objects.get(nombre="Artesanías")
        feria, errors = Feria.new(
            "Mercado de Diseño",
            categoria,
            date(2026, 8, 1),
            date(2026, 8, 3),
            "Muelle Turístico",
            15,
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(feria)
        self.assertEqual(feria.nombre, "Mercado de Diseño")
        self.assertTrue(Feria.objects.filter(nombre="Mercado de Diseño").exists())

    def test_new_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Feria.objects.count()
        feria, errors = Feria.new("", "", None, None, "", 0)
        self.assertIsNone(feria)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Feria.objects.count(), count_antes)

    # --- update ---

    def test_update_modifica_datos_correctamente(self):
        errors = self.feria.update(
            "Feria de Invierno",
            self.feria.categoria,
            date(2026, 7, 1),
            date(2026, 7, 3),
            "Parque Central",
            20,
        )
        self.assertEqual(errors, [])
        self.feria.refresh_from_db()
        self.assertEqual(self.feria.ubicacion, "Parque Central")
        self.assertEqual(self.feria.capacidad_puestos, 20)

    def test_update_con_datos_invalidos_no_modifica(self):
        errors = self.feria.update("", "", None, None, "", 0)
        self.assertTrue(len(errors) > 0)
        self.feria.refresh_from_db()
        self.assertEqual(self.feria.nombre, "Feria de Invierno")  # sin cambios

    def test_puestos_ocupados_cuenta_solo_confirmadas(self):
        # crear usuario y emprendedor para las inscripciones
        user = User.objects.create_user(username="u_test", password="pass")
        emprendedor = Emprendedor.objects.create(
            nombre="Juan",
            apellido="Perez",
            rubro="Artes",
            telefono="+54123456789",
            usuario=user,
        )
        # inscripciones: una confirmada y otra cancelada
        Inscripcion.objects.create(
            feria=self.feria,
            emprendedor=emprendedor,
            numero_puesto=1,
            estado="confirmada",
        )
        Inscripcion.objects.create(
            feria=self.feria,
            emprendedor=emprendedor,
            numero_puesto=2,
            estado="cancelada",
        )
        self.assertEqual(self.feria.puestos_ocupados(), 1)
        self.assertEqual(self.feria.puestos_disponibles(), 9)

    def test_duracion_dias(self):
        # en setUp la feria tiene fecha_inicio 2026-07-01 y fecha_fin 2026-07-03 => 3 días
        self.assertEqual(self.feria.duracion_dias(), 3)

    def test_is_activa_method(self):
        self.assertTrue(self.feria.is_activa())
        self.feria.activa = False
        self.feria.save()
        self.assertFalse(self.feria.is_activa())



    # TODO: agregar tests para Emprendedor e Inscripcion cuando los implementen:
    # def test_tiene_lugar_false_cuando_llena(self): ...
    # def test_puestos_ocupados_cuenta_solo_confirmadas(self): ...

