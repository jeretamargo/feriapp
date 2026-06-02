from django import forms
from ..models import Sector
from django.utils import timezone

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"  , "placeholder": "Nombre del sector", "required": True}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción del sector", "required": True, "rows": 4}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre and len(nombre.strip()) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre.strip()