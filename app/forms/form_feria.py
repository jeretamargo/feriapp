
from django import forms
from ..models import Feria
from django.utils import timezone


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

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        
        

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
        
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre and len(nombre.strip()) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre.strip()
    
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get("fecha_inicio")
        if fecha_inicio and fecha_inicio < timezone.now().date():
            raise forms.ValidationError("La fecha de inicio no puede ser en el pasado.")
        return fecha_inicio
    
    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get("fecha_fin")
        if fecha_fin and fecha_fin < timezone.now().date():
            raise forms.ValidationError("La fecha de fin no puede ser en el pasado.")
        return fecha_fin
    