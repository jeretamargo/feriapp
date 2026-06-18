from django.test import TestCase
from usuarios.models.user_models import User
from django.contrib.auth.models import Group
class UserTest(TestCase):

    def setUp(self):
        
        self.userAdmin = User.objects.create_superuser(
            username="jere",
            password="123456",
            
        )
        self.userEmprendedor = User.objects.create_user(
            username="MaxPayne",
            password="123456",
        )
        self.userVisitante = User.objects.create_user(
            username="PhillCollins",
            password="123456",
        )

        self.grupoEmprendedor,_ = Group.objects.get_or_create(name="Emprendedor")
        self.grupoVisitante,_ = Group.objects.get_or_create(name="Visitante")
        
        
        self.userEmprendedor.groups.add(self.grupoEmprendedor)
        self.userVisitante.groups.add(self.grupoVisitante)

    def test_es_emprendedor_true(self):
        self.assertTrue(self.userEmprendedor.es_emprendedor())
        

    def test_es_emprendedor_false(self):
        self.assertFalse(self.userVisitante.es_emprendedor())
        

    def test_es_visitante_true(self):
        self.assertTrue(self.userVisitante.es_visitante())
    
    
    def test_es_visitante_false(self):
        self.assertFalse(self.userEmprendedor.es_visitante())
        

    def test_es_superuser_true(self):
        self.assertTrue(self.userAdmin.is_superuser)
        
    
    def test_es_superuser_false(self):
        self.assertFalse(self.userEmprendedor.is_superuser)
        self.assertFalse(self.userVisitante.is_superuser)
        