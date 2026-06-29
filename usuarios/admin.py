from django.contrib import admin
from app.models.inscripcion_models import Inscripcion
from app.models.resena_models import Resena
from usuarios.models.emprendedor_models import Emprendedor
from usuarios.models.user_models import User
from usuarios.models.visitante_models import Visitante
from usuarios.models.notificacion_models import Notificacion
# Register your models here.



class ResenaInline(admin.TabularInline):
    model = Resena
    extra = 0
    


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo_usuario' )

  
    list_filter = ('tipo_usuario',)

    
    search_fields = ('username', 'email', 'tipo_usuario')
   
    list_per_page = 10
    fieldsets = (
    ('Información Principal', {
    'fields': ('username', 'email', 'password')
    }),
    
    ('Permisos', {
    'fields': ('groups','is_superuser')
    }),
    )
    
    

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'rubro', 'telefono','usuario__username', 'usuario__email'  )

  
    list_filter = ('rubro',)

    
    search_fields = ('nombre', 'apellido','usuario__username','rubro', 'usuario__email')
   
    list_per_page = 10

    fieldsets = (
 ('Información Principal', {
 'fields': ('nombre', 'apellido', 'rubro')
 }),
 ('Contacto', {
 'fields': ('telefono',)
 }),
 ('Usuario correspondiente', {
 'fields': ('usuario',)
 }),
 )
    inlines=[InscripcionInline, ResenaInline]
    
    

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'usuario__username', 'usuario__email'  )

  
    
    
    search_fields = ('nombre', 'apellido','usuario__username', 'usuario__email')
   
    list_per_page = 10

    fieldsets = (
 ('Información Principal', {
 'fields': ('nombre', 'apellido')
 }),
 
 ('Usuario correspondiente', {
 'fields': ('usuario',)
 }),
 )
    inlines=[ResenaInline]

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
     list_display = ('usuario__username', 'asunto', 'mensaje', 'leida','fecha_creacion' )

  
     list_filter = ('asunto',)

    
     search_fields = ('usuario__username', 'mensaje')
   
     list_per_page = 10
    