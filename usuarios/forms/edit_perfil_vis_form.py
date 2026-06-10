from django import forms
from django.forms import ModelForm

from usuarios.models.visitante_models import Visitante

class VisitanteUpdateForm(ModelForm):
    class Meta:
        model = Visitante
        fields = [
            "nombre",
            "apellido",
        ]

    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre",
            }
        )
    )
    apellido = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Apellido",
            }
        )
    )

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
    
    def save(self):
        visitante = self.instance

        errores = visitante.update(
            nombre=self.cleaned_data["nombre"],
            apellido=self.cleaned_data["apellido"]
        )

        if errores:
            for error in errores:
                self.add_error(None, error)

        return visitante