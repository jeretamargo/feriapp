
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models.user_models import User
from usuarios.models.visitante_models import Visitante
from django.contrib.auth.models import Group
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
    def clean_username(self):
       username = self.cleaned_data.get("username")
       if not username or not username.strip():
            raise forms.ValidationError("El nombre de usuario es obligatorio.")
       return username.strip()
    
    def clean_nombre(self):
       nombre = self.cleaned_data.get("nombre")
       if nombre and len(nombre.strip()) <= 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
       return nombre.strip()
    
    def clean_apellido(self):
       apellido = self.cleaned_data.get("apellido")
       if apellido and len(apellido.strip()) <= 3:
            raise forms.ValidationError("El apellido debe tener al menos 3 caracteres.")
       return apellido.strip()
    
    
    def clean_email(self):
        email= self.cleaned_data.get("email")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise forms.ValidationError("Ingrese un email válido.")
        return email
    
    def clean_password1(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("password1")
        if username and username.lower() in password1.lower():
            raise forms.ValidationError(
                "La contraseña no puede contener el nombre de usuario."
            )

        if email:
            parte_email = email.split("@")[0]
            if parte_email.lower() in password1.lower():
                raise forms.ValidationError(
                    "La contraseña no puede contener el email."
                )
        
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$", password1):
            raise forms.ValidationError("Debe tener al menos 8 caracteres, una letra y un número.")
        return password1.strip()    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = "visitante"
        if commit:
         user.save()
        errores = Visitante.new(
            usuario=user,
            nombre=self.cleaned_data["nombre"],
            apellido=self.cleaned_data["apellido"],
        
        )
        if errores:
            for error in errores:
                self.add_error(None, error)
        grupo = Group.objects.get(name="Visitante")
        user.groups.add(grupo)
        return user
