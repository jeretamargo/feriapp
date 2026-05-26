
from django import forms
from ..models import Feria

class FeriaForm(forms.ModelForm):
    class Meta:
        model = Feria
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"  , "placeholder": "Nombre de la feria", "required": True}),
            "categoria": forms.Select(attrs={"class": "form-select","required": True}),
            "fecha_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d"
            ),
            "fecha_fin": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d"
            ),
            "ubicacion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ubicación de la feria", "required": True}),
            "capacidad_puestos": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Capacidad de puestos", "required": True, "min": 1}),
            "activa": forms.CheckboxInput(attrs={"class": "form-check-input", "default": False}),
        }
