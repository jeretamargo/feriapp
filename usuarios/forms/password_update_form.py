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