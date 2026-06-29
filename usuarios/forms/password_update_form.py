import re

from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class PasswordUpdateForm(PasswordChangeForm):

    

    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese su contraseña actual",
            }
        )
    )

    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese la nueva contraseña",
            }
        )
    )

    new_password2 = forms.CharField(
        label="Repita la nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Repita la nueva contraseña",
            }
        )
    )

    def clean_new_password1(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("new_password1")
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