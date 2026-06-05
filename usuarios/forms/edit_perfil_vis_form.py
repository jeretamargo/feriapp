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
        nombre = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            "placeholder": "Nombre"
        }
    ))
        apellido = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            "placeholder": "Apellido"
        }
    ))
