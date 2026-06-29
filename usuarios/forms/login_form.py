from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.urls import reverse_lazy

class LoginForm(AuthenticationForm):
       username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese su usuario",
            }
        )
    )

       password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese su contraseña",
            }
        )
    )
        # o la vista que quieras

