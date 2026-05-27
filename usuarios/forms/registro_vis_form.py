from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models.user_models import User

class RegistroVisitanteForm(UserCreationForm):
    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "tipo_usuario",
            "password1",
            "password2",
        )
    
    username = forms.CharField()
    widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Usuario"
        }
    )

    email = forms.EmailField()
    widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Correo electrónico"
        }
    )
    tipo_usuario = forms.ChoiceField(choices=User.TIPO_USUARIO)
    widget=forms.Select(
        attrs={
            "class": "form-control",
            "placeholder": "Tipo de usuario"
        }
    )
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
