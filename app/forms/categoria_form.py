
from django import forms
from ..models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"  , "placeholder": "Nombre de la feria", "required": True}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción de la feria", "required": True}),
        }


