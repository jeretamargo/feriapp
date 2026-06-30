from django.test import TestCase
from usuarios.models.user_models import User
from usuarios.models.notificacion_models import Notificacion

class NotificacionTest(TestCase):
    def setUp(self):
        
        self.userEmprendedor = User.objects.create_user(
            username="MaxPayne",
            password="123456",
            
        )
        
    def test_validate_return_errors(self):
            errors1 = Notificacion.validate(
                asunto="Inscripción Exitosa",
                mensaje="",
                usuario=self.userEmprendedor,
                
            )
            errors2 = Notificacion.validate(
                asunto="",
                mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
                usuario=self.userEmprendedor
            )
            errors3 = Notificacion.validate(
                asunto="Inscripción Exitosa",
                mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
                usuario=None
                
            )
            self.assertIn("El mensaje es obligatorio",errors1)
            self.assertIn("El asunto es obligatorio",errors2)
            self.assertIn("No existe usuario asignado a la notificación",errors3)

    def test_validate_works_ok(self):
        errors = Notificacion.validate(
            asunto="Inscripción Exitosa",
            mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
            usuario=self.userEmprendedor
        )
        self.assertEqual(errors, [])
    
    def test_new_handle_errors(self):
        notificacion,errors = Notificacion.new(
            asunto="",
            mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
            usuario=self.userEmprendedor,
            url="#"
        )
        self.assertNotEqual([], errors)

        self.assertIsNone(notificacion)

        self.assertNotEqual( Notificacion.objects.count(), 1)

    def test_new_works_ok(self):
        notificacion, errors = Notificacion.new(
           asunto="Inscripción Exitosa",
           mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
           usuario=self.userEmprendedor,
           url="#"
        )
        self.assertEqual([], errors)

        self.assertIsNotNone(notificacion)

        self.assertEqual(Notificacion.objects.count(), 1)

    def test_update_handle_errors(self):
        notificacion, _ = Notificacion.new(
           asunto="Inscripción Exitosa",
           mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
           usuario=self.userEmprendedor,
           url="#"
        )
        errors = notificacion.update(
           asunto="",
           mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
           usuario=self.userEmprendedor,
           url="#")
        
        self.assertIn("El asunto es obligatorio", errors)
        self.assertEqual(notificacion.asunto, "Inscripción Exitosa")

    def test_update_works_ok(self):
        notificacion, _= Notificacion.new(
           asunto="Inscripción Exitosa",
           mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
           usuario=self.userEmprendedor,
           url="#"
        )
        errors = notificacion.update(
           asunto="Inscripción Exitosa",
           mensaje="Se ha inscripto a la feria 'Artesanias del fuego' correctamente",
           usuario=self.userEmprendedor,
           url="#"
        )
        self.assertEqual(errors, [])
        self.assertEqual(notificacion.mensaje, "Se ha inscripto a la feria 'Artesanias del fuego' correctamente")

    def test_leida_works_ok(self):
     notificacion, _= Notificacion.new(
           asunto="Inscripción Exitosa",
           mensaje="Se ha inscripto a la feria 'Arte del sur' correctamente",
           usuario=self.userEmprendedor,
           url="#"
        )
     notificacion.marcar_leida()
     self.assertTrue(notificacion.leida)