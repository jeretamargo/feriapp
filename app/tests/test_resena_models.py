from datetime import date

from django.test import TestCase
from django.db import IntegrityError

from app.models.categoria_models import Categoria
from app.models.feria_models import Feria
from app.models.sector_models import Sector
from usuarios.models import Emprendedor, User
from app.models import Inscripcion, Resena


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