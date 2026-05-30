from django.contrib import admin
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User
from usuarios.models.visitante_models import Visitante
from usuarios.models.notificacion_models import Notificacion
# Register your models here.
admin.site.register(User)
admin.site.register(Emprendedor)
admin.site.register(Visitante)
admin.site.register(Notificacion)