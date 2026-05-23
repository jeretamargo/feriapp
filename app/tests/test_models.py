"""Tests de comportamiento para el modelo Feria."""

from datetime import date

from django.test import TestCase

from app.models import Categoria, Feria, Inscripcion, Resena
#para hacer los test de resena y inscripcion 
from usuarios.models import User, Emprendedor


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

    # TODO: agregar tests para Emprendedor e Inscripcion cuando los implementen:
    # def test_tiene_lugar_false_cuando_llena(self): ...
    # def test_puestos_ocupados_cuenta_solo_confirmadas(self): ...


class InscripcionModelTest(TestCase):

    def setUp(self):
        categoria = Categoria.objects.create(
            nombre="Artesanías"
        )

        self.feria = Feria.objects.create(
            nombre="Feria Test",
            categoria=categoria,
            fecha_inicio=date(2026, 7, 1),
            fecha_fin=date(2026, 7, 3),
            ubicacion="Plaza",
            capacidad_puestos=10,
        )

        self.user = User.objects.create_user(
            username="juan",
            password="1234"
        )

        self.emprendedor = Emprendedor.objects.create(
            nombre="juancho",
            apellido="perez",
            rubro="Comida",
            telefono="123456789",
            usuario=self.user
        )

    # para el validate

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        errors = Inscripcion.validate(
            self.feria,
            self.emprendedor,
            1,
            "confirmada"
        )

        self.assertEqual(errors, [])

    def test_validate_numero_puesto_invalido_retorna_error(self):
        errors = Inscripcion.validate(
            self.feria,
            self.emprendedor,
            0,
            "confirmada"
        )

        self.assertTrue(len(errors) > 0)

    #new

    def test_new_crea_inscripcion(self):
        inscripcion, errors = Inscripcion.new(
            self.feria,
            self.emprendedor,
            1,
            "confirmada"
        )

        self.assertEqual(errors, [])
        self.assertIsNotNone(inscripcion)

        self.assertTrue(
            Inscripcion.objects.filter(
                feria=self.feria,
                emprendedor=self.emprendedor
            ).exists()
        )

    #update

    def test_update_modifica_estado_y_puesto(self):

        inscripcion = Inscripcion.objects.create(
            feria=self.feria,
            emprendedor=self.emprendedor,
            numero_puesto=1,
            estado="confirmada"
        )

        errors = inscripcion.update(
            2,
            "cancelada"
        )

        self.assertEqual(errors, [])

        inscripcion.refresh_from_db()

        self.assertEqual(inscripcion.numero_puesto, 2)
        self.assertEqual(inscripcion.estado, "cancelada")


class ResenaModelTest(TestCase):

    def setUp(self):

        categoria = Categoria.objects.create(
            nombre="Tecnología"
        )

        self.feria = Feria.objects.create(
            nombre="Expo Tech",
            categoria=categoria,
            fecha_inicio=date(2026, 8, 1),
            fecha_fin=date(2026, 8, 3),
            ubicacion="Centro Cultural",
            capacidad_puestos=20,
        )

        self.user = User.objects.create_user(
            username="maria",
            password="1234"
        )

        self.emprendedor = Emprendedor.objects.create(
            nombre="maria",
            apellido="eskelope",
            rubro="electronica",
            telefono="987654321",
            usuario=self.user
        )

    # para validate

    def test_validate_datos_correctos_retorna_lista_vacia(self):

        errors = Resena.validate(
            self.feria,
            self.emprendedor,
            "excelente feria",
            5
        )

        self.assertEqual(errors, [])

    def test_validate_puntuacion_fuera_de_rango_retorna_error(self):

        errors = Resena.validate(
            self.feria,
            self.emprendedor,
            "Comentario",
            10
        )

        self.assertTrue(len(errors) > 0)

    # nueva resena
    def test_new_crea_resena(self):
        resena, errors = Resena.new(
            self.feria,
            self.emprendedor,
            "muy buena experiencia",
            5
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(resena)

        self.assertTrue(
            Resena.objects.filter(
                feria=self.feria,
                emprendedor=self.emprendedor
            ).exists()
        )

    #update
    def test_update_modifica_comentario_y_puntuacion(self):

        resena = Resena.objects.create(
            feria=self.feria,
            emprendedor=self.emprendedor,
            comentario="viiejo comentario",
            puntuacion=3
        )
        errors = resena.update(
            "nuevo comentario",
            5
        )

        self.assertEqual(errors, [])

        resena.refresh_from_db()

        self.assertEqual(
            resena.comentario,
            "Nuevo comentario"
        )

        self.assertEqual(
            resena.puntuacion,
            5
        )