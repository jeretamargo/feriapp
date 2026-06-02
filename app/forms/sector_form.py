from django import forms
from ..models import Sector
from django.utils import timezone

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"  , "placeholder": "Nombre del sector", "required": True}),
            "capacidad_puestos": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Capacidad de puestos", "required": True, "min": 1}),
            "tiene_conexion_electrica": forms.CheckboxInput(attrs={"class": "form-check-input", "default": False}),
            "edicion": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d"
            ),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre and len(nombre.strip()) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre.strip()
    
    def clean_edicion(self):
        edicion = self.cleaned_data.get("edicion")
        if edicion and edicion < timezone.now().date():
            raise forms.ValidationError("La edición no puede ser en el pasado.")
        return edicion
    
    def clean_capacidad_puestos(self):
        capacidad_puestos = self.cleaned_data.get("capacidad_puestos")
        if capacidad_puestos is not None and capacidad_puestos <= 0:
            raise forms.ValidationError("La capacidad de puestos debe ser mayor a cero.")
        return capacidad_puestos
    
    
        