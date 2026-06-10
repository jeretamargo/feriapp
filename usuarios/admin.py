from django.contrib import admin
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User
from usuarios.models.visitante_models import Visitante
from usuarios.models.notificacion_models import Notificacion
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    pass

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    pass

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    pass