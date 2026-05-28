from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models.user_models import User
from usuarios.models.visitante_models import Visitante

class RegistroVisitanteForm(UserCreationForm):
    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
    
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Usuario"
        }
    ))
    
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Nombre"
        }
    ))
    
    apellido = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Apellido"
        }
    ))
    

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Correo electrónico"
        }
    ))
    
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Contraseña"
        }
    ))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Confirmar contraseña"
        }
    ))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = "visitante"
        if commit:
         user.save()
        Visitante.new(
            usuario=user,
            nombre=self.cleaned_data["nombre"],
            apellido=self.cleaned_data["apellido"],
        
        )
        return user
