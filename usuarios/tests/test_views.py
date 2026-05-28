from django.test import TestCase
from django.urls import reverse

from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User

# Create your tests here.

class EmprendedorListViewTest(TestCase):
    """Tests para EmprendedorListView (ListView)"""

    def setUp(self):
        self.user1= User.objects.create(
            username="maxpayne01",
            password="pbkdf2_sha256$720000$fakehash$fakehash",
            email="max.payne01@gmail.com"
        )
        self.user2= User.objects.create(
            username="phillyc",
            password="pbkdf2_sha256$720001$fakehash$fakehash",
            email="phill.collins.og@gmail.com"
        )

        self.emp1 = Emprendedor.objects.create(
            nombre = "Max",
            apellido = "Payne",
            rubro = "Analgésicos y Munición de armas de fuego",
            telefono = "+54 2901 111111",
            usuario = self.user1
        )
        self.emp2 = Emprendedor.objects.create(
            nombre = "Phill",
            apellido = "Collins",
            rubro = "Instrumentos Musicales",
            telefono = "+54 2901 111111",
            usuario = self.user2
        )

    def test_lista_responde_200(self):
        response = self.client.get(reverse("usuarios:lista_emprendedores"))
        self.assertEqual(response.status_code, 200)

    def test_lista_contiene_ambos_emprendedores(self):
        response = self.client.get(reverse("usuarios:lista_emprendedores"))
        self.assertEqual(len(response.context["emprendedores"]), 2)

    def test_lista_vacia_responde_200(self):
        Emprendedor.objects.all().delete()
        response = self.client.get(reverse("usuarios:lista_emprendedores"))
        self.assertEqual(response.status_code, 200)

    
