from django.contrib import admin
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User
from usuarios.models.visitante_models import Visitante
from usuarios.models.notificacion_models import Notificacion
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo_usuario' )

  
    list_filter = ('tipo_usuario',)

    
    search_fields = ('username', 'email', 'tipo_usuario')
   
    list_per_page = 10
    

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'rubro', 'telefono','usuario__username', 'usuario__email'  )

  
    list_filter = ('rubro',)

    
    search_fields = ('nombre', 'apellido','usuario__username','rubro', 'usuario__email')
   
    list_per_page = 10
    
    

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'usuario__username', 'usuario__email'  )

  
    
    
    search_fields = ('nombre', 'apellido','usuario__username', 'usuario__email')
   
    list_per_page = 10
    pass

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
     list_display = ('usuario__username', 'asunto', 'mensaje', 'leida','fecha_creacion' )

  
     list_filter = ('asunto',)

    
     search_fields = ('usuario__username', 'mensaje')
   
     list_per_page = 10
    