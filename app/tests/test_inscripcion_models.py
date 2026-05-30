from datetime import date

from django.test import TestCase

from app.models.categoria_models import Categoria
from app.models.feria_models import Feria
from app.models.inscripcion_models import Inscripcion
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User


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

