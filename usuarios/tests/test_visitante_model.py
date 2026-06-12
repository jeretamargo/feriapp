from django.test import TestCase
from usuarios.models.user_models import User
from usuarios.models.visitante_models import Visitante
class VisitanteTest(TestCase):
    def setUp(self):
        self.userVisitante1 = User.objects.create_user(
            username="MaxPayne",
            password="123456",
        )
        self.userVisitante2 = User.objects.create_user(
            username="PhillyC",
            password="123456",
        )
        
        
    def test_validate_return_errors(self):
        errors1 = Visitante.validate(
            nombre="Max",
            apellido="",
            usuario=self.userVisitante1
        )
        errors2 = Visitante.validate(
            nombre="",
            apellido="Payne",
            usuario=self.userVisitante1
        )
        errors3 = Visitante.validate(
            nombre="Max",
            apellido="Payne",
            usuario=None
            
        )
        self.assertIn("El apellido es obligatorio",errors1)
        self.assertIn("El nombre es obligatorio",errors2)
        self.assertIn("El user es obligatorio",errors3)

    def test_validate_works_ok(self):
        errors = Visitante.validate(
            nombre="Max",
            apellido="Payne",
            usuario=self.userVisitante1
        )
        self.assertEqual(errors, [])
    
    def test_new_handle_errors(self):
        visitante,errors = Visitante.new(
            nombre="Max",
            apellido="",
            usuario=self.userVisitante1
        )
        self.assertNotEqual([], errors)

        self.assertIsNone(visitante)

        self.assertNotEqual( Visitante.objects.count(), 1)

    def test_new_works_ok(self):
        visitante, errors = Visitante.new(
            nombre="Max",
            apellido="Collins",
            usuario=self.userVisitante1
        )
        self.assertEqual([], errors)

        self.assertIsNotNone(visitante)

        self.assertEqual( Visitante.objects.count(), 1)

    def test_update_handle_errors(self):
        visitante, _ = Visitante.new(
            nombre="Phill",
            apellido="Collins",
            usuario=self.userVisitante2
        )
        errors = visitante.update(
            nombre="Phill",
            apellido="",
            usuario=self.userVisitante2)
        
        self.assertIn("El apellido es obligatorio", errors)
        self.assertEqual(visitante.apellido, "Collins")

    def test_update_works_ok(self):
        visitante, _= Visitante.new(
            nombre="Phill",
            apellido="Collins",
            usuario=self.userVisitante2
        )
        errors = visitante.update(
            nombre="Philly",
            apellido="Collins",
            usuario=self.userVisitante2)
        
        self.assertEqual(errors, [])
        self.assertEqual(visitante.nombre, "Philly")

    def test_nombreCompleto_works(self):
        visitante1 , _ = Visitante.new(
            nombre="Max",
            apellido="Payne",
            usuario=self.userVisitante1
        )
        visitante2 , _= Visitante.new(
            nombre="Phill",
            apellido="Collins",
            usuario=self.userVisitante2
        )
        
        self.assertEqual(visitante1.nombre_completo(),"Max Payne")
        self.assertEqual(visitante2.nombre_completo(),"Phill Collins")
    

