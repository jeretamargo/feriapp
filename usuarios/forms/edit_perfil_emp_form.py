from django import forms
from django.forms import ModelForm

from usuarios.models.emprendedor_models import Emprendedor
class EmprendedorUpdateForm(ModelForm):
    class Meta:
        model = Emprendedor
        fields = [
            "nombre",
            "apellido",
            "telefono",
            "rubro"
        ]

    nombre = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            
        }
    ))
    apellido = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            
        }
    ))
    telefono = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            
        }
    ))
    rubro = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            
        }
    ))
    