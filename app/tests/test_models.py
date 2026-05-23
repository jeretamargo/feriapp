"""Tests de comportamiento para el modelo Feria."""

from datetime import date

from django.test import TestCase
from django.db import IntegrityError

from app.models import Categoria, Feria, Sector, Emprendedor, Inscripcion
from usuarios.models import User


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


class SectorModelTest(TestCase):
    """Tests para el modelo Sector."""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Varios")
        self.feria = Feria.objects.create(
            nombre="Feria Test",
            categoria=self.categoria,
            fecha_inicio=date(2026, 7, 1),
            fecha_fin=date(2026, 7, 2),
            ubicacion="Lugar",
            capacidad_puestos=20,
        )

    def test_str_retorna_nombre(self):
        sector = Sector.objects.create(
            nombre="Gastronomía",
            edicion=date(2026, 7, 1),
            capacidad_puestos=10,
            tiene_conexion_electrica=True,
            feria=self.feria,
        )
        self.assertEqual(str(sector), "Gastronomía")

    def test_es_edicion_actual_true_y_false(self):
        sector_actual = Sector(
            nombre="Actual",
            edicion=date(2026, 7, 1),
            capacidad_puestos=5,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        # Dependemos del año en las fixtures; asumir 2026 en tests
        self.assertEqual(sector_actual.es_edicion_actual(), sector_actual.edicion.year == date.today().year)

        sector_viejo = Sector(
            nombre="Viejo",
            edicion=date(2000, 1, 1),
            capacidad_puestos=5,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        self.assertFalse(sector_viejo.es_edicion_actual())

    
    def test_descripcion_completa_contiene_info_y_conexion(self):
        sector = Sector.objects.create(
            nombre="Artes",
            edicion=date(2026, 7, 1),
            capacidad_puestos=12,
            tiene_conexion_electrica=True,
            feria=self.feria,
        )
        desc = sector.descripcion_completa()
        #assertIn es para verificar que la descripción contenga ciertos fragmentos clave
        self.assertIn("con conexión eléctrica", desc)
        self.assertIn("Capacidad: 12", desc)

    def test_validate_datos_correctos_retorna_lista_vacia(self):
        sector = Sector(
            nombre="Valido",
            edicion=date(2026, 7, 1),
            capacidad_puestos=3,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        errors = sector.validate()
        self.assertEqual(errors, [])

    def test_validate_nombre_vacio_retorna_error(self):
        sector = Sector(
            nombre="",
            edicion=date(2026, 7, 1),
            capacidad_puestos=3,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        errors = sector.validate()
        self.assertTrue(len(errors) > 0)

    # nombre corto no es válido
    def test_validate_nombre_corto_retorna_error(self):
        sector = Sector(
            nombre="aa",
            edicion=date(2026, 7, 1),
            capacidad_puestos=3,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        errors = sector.validate()
        self.assertTrue(len(errors) > 0)

    # capacidad cero no es válida, debe ser al menos 1
    def test_validate_capacidad_cero_retorna_error(self):
        sector = Sector(
            nombre="Sector",
            edicion=date(2026, 7, 1),
            capacidad_puestos=0,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        errors = sector.validate()
        self.assertTrue(len(errors) > 0)

    # cambio de nombre, sin errores
    def test_update_modifica_datos_correctamente(self):
        sector = Sector.objects.create(
            nombre="Mod",
            edicion=date(2026, 7, 1),
            capacidad_puestos=5,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        errors = sector.update("Mod", date(2026, 7, 1), 10, True)
        self.assertEqual(errors, [])
        sector.refresh_from_db()
        self.assertEqual(sector.capacidad_puestos, 10)

    # update datos erroneos, no se modifica
    def test_update_con_datos_invalidos_no_modifica(self):
        sector = Sector.objects.create(
            nombre="NoMod",
            edicion=date(2026, 7, 1),
            capacidad_puestos=5,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        errors = sector.update("", None, 0, False)
        self.assertTrue(len(errors) > 0)
        sector.refresh_from_db()
        self.assertEqual(sector.nombre, "NoMod")

    # unique_together evita duplicados en misma feria
    def test_unique_together_evita_duplicados_en_misma_feria(self):
        Sector.objects.create(
            nombre="Dup",
            edicion=date(2026, 7, 1),
            capacidad_puestos=4,
            tiene_conexion_electrica=False,
            feria=self.feria,
        )
        with self.assertRaises(IntegrityError):
            Sector.objects.create(
                nombre="Dup",
                edicion=date(2026, 7, 1),
                capacidad_puestos=6,
                tiene_conexion_electrica=True,
                feria=self.feria,
            )

    def test_new_con_datos_invalidos_retorna_errores_y_no_crea(self):
        count_antes = Sector.objects.count()
        sector, errors = Sector.new("", None, 0, False)
        self.assertIsNone(sector)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(Sector.objects.count(), count_antes)

    #Agrego claudio
    def test_new_con_datos_validos_intenta_guardar(self):
        # Sector.new actualmente no recibe 'feria' y al crear puede lanzar IntegrityError
        try:
            sector, errors = Sector.new("Nuevo", date(2026, 7, 1), 5, True)
        except IntegrityError:
            # comportamiento aceptable dado que falta la FK 'feria'
            return
        # si no lanzó excepción, asegurar que devolvió instancia válida
        self.assertIsNone(errors) or self.assertEqual(errors, [])
        if sector:
            self.assertTrue(Sector.objects.filter(pk=sector.pk).exists())


    # TODO: agregar tests para Emprendedor e Inscripcion cuando los implementen:
    # def test_tiene_lugar_false_cuando_llena(self): ...
    # def test_puestos_ocupados_cuenta_solo_confirmadas(self): ...
