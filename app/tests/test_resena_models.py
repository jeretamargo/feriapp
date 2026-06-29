
from django.test import TestCase



from app.models import  Resena
from usuarios.models.visitante_models import Visitante
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User

class ResenaModelTest(TestCase):

    def setUp(self):
        self.visitante_user = User.objects.create_user(
        username="juan",
        password="1234"
        )

        self.visitante = Visitante.objects.create(
        nombre="Juan",
        apellido="Perez",
        usuario=self.visitante_user
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
        self.visitante,
        self.emprendedor,
        "excelente feria",
        5
        )

        self.assertEqual(errors, [])

    def test_validate_puntuacion_fuera_de_rango_retorna_error(self):

        errors = Resena.validate(
        self.visitante,
        self.emprendedor,
        "Comentario",
        10
        )

        self.assertTrue(len(errors) > 0)

    # nueva resena
    def test_new_crea_resena(self):
        resena, errors = Resena.new(
            self.visitante,
            self.emprendedor,
            "muy buena experiencia",
            5
        )
        self.assertEqual(errors, [])
        self.assertIsNotNone(resena)

        self.assertTrue(
            Resena.objects.filter(
                visitante=self.visitante,
                emprendedor=self.emprendedor
            ).exists()
        )

    #update
    def test_update_modifica_comentario_y_puntuacion(self):

        resena = Resena.objects.create(
            visitante=self.visitante,
            emprendedor=self.emprendedor,
            comentario="viejo comentario",
            puntuacion=3
        )
        errors = resena.update(
            "Nuevo comentario",
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