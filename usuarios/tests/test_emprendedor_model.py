from django.test import TestCase
from usuarios.models.user_models import User
from usuarios.models.emprendedor_models import Emprendedor
from django.contrib.auth.models import Group
class EmprendedorTest(TestCase):
    def setUp(self):
        self.userEmprendedor1 = User.objects.create_user(
            username="MaxPayne",
            password="123456",
        )
        self.userEmprendedor2 = User.objects.create_user(
            username="PhillyC",
            password="123456",
        )
        
        
    def test_validate_return_errors(self):
        errors1 = Emprendedor.validate(
            nombre="Max",
            apellido="Payne",
            rubro="",
            telefono="2901123456",
            usuario=self.userEmprendedor1
        )
        errors2 = Emprendedor.validate(
            nombre="",
            apellido="Payne",
            rubro="Venta de Analgésicos",
            telefono="2901123456",
            usuario=self.userEmprendedor1
        )
        errors3 = Emprendedor.validate(
            nombre="Max",
            apellido="Payne",
            rubro="Venta de Analgésicos",
            telefono="2901123456",
            usuario=None
            
        )
        errors4 = Emprendedor.validate(
            nombre="Max",
            apellido="",
            rubro="Venta de Analgésicos",
            telefono="2901123456",
            usuario=None
            
        )
        errors5 = Emprendedor.validate(
            nombre="Max",
            apellido="Payne",
            rubro="Venta de Analgésicos",
            telefono="",
            usuario=None
            
        )
        self.assertIn("El rubro es obligatorio",errors1)
        self.assertIn("El nombre es obligatorio",errors2)
        self.assertIn("El user es obligatorio",errors3)
        self.assertIn("El apellido es obligatorio",errors4)
        self.assertIn("El numero de teléfono es obligatorio",errors5)

    def test_validate_works_ok(self):
        errors = Emprendedor.validate(
            nombre="Max",
            apellido="Payne",
            rubro="Venta de Analgésicos",
            telefono="2901123456",
            usuario=self.userEmprendedor1
        )
        self.assertEqual(errors, [])
    
    def test_new_handle_errors(self):
        emprendedor,errors = Emprendedor.new(
            nombre="Max",
            apellido="",
            rubro="Venta de Analgésicos",
            telefono="2901123456",
            usuario=self.userEmprendedor1
        )
        self.assertNotEqual([], errors)

        self.assertIsNone(emprendedor)

        self.assertNotEqual( Emprendedor.objects.count(), 1)

    def test_new_works_ok(self):
        emprendedor, errors = Emprendedor.new(
            nombre="Max",
            apellido="Payne",
            rubro="Venta de Analgésicos",
            telefono="2901123456",
            usuario=self.userEmprendedor1
        )
        self.assertEqual([], errors)

        self.assertIsNotNone(emprendedor)

        self.assertEqual( Emprendedor.objects.count(), 1)

    def test_update_handle_errors(self):
        emprendedor, errors = Emprendedor.new(
            nombre="Phill",
            apellido="Collins",
            rubro="Venta Instrumentos Musicales",
            telefono="2901123456",
            usuario=self.userEmprendedor2
        )
        errors = emprendedor.update(
            nombre="Phill",
            apellido="Collins",
            rubro="",
            telefono="2901123456",
            usuario=self.userEmprendedor2)
        
        self.assertIn("El rubro es obligatorio", errors)
        self.assertEqual(emprendedor.rubro, "Venta Instrumentos Musicales")

    def test_update_works_ok(self):
        emprendedor, _= Emprendedor.new(
            nombre="Phill",
            apellido="Collins",
            rubro="Venta Instrumentos Musicales",
            telefono="2901123456",
            usuario=self.userEmprendedor2
        )
        errors = emprendedor.update(
            nombre="Phill",
            apellido="Collins",
            rubro="Venta Instrumentos Musicales y Micrófonos",
            telefono="2901123456",
            usuario=self.userEmprendedor2)
        
        self.assertEqual(errors, [])
        self.assertEqual(emprendedor.rubro, "Venta Instrumentos Musicales y Micrófonos")

    def test_nombreCompleto_works(self):
        emprendedor1 , _ = Emprendedor.new(
            nombre="Max",
            apellido="Payne",
            rubro="Venta de Analgésicos",
            telefono="2901123456",
            usuario=self.userEmprendedor1
        )
        emprendedor2 , _= Emprendedor.new(
            nombre="Phill",
            apellido="Collins",
            rubro="Venta Instrumentos Musicales",
            telefono="2901123456",
            usuario=self.userEmprendedor2
        )
        
        self.assertEqual(emprendedor1.nombre_completo(),"Max Payne")
        self.assertEqual(emprendedor2.nombre_completo(),"Phill Collins")
    

