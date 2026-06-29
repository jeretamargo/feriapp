
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
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        return cleaned_data
                
    
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
    
    def clean_capacidad_puestos(self):
        capacidad_puestos = self.cleaned_data.get("capacidad_puestos")
        if capacidad_puestos is not None and capacidad_puestos <= 0:
            raise forms.ValidationError("La capacidad de puestos debe ser mayor a cero.")
        return capacidad_puestos
    
    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get("ubicacion")
        if not ubicacion or not ubicacion.strip():
            raise forms.ValidationError("La ubicación de la feria es obligatoria.")
        return ubicacion.strip()
    
    def clean_categoria(self):
        categoria = self.cleaned_data.get("categoria")
        if not categoria:
            raise forms.ValidationError("La categoría de la feria es obligatoria.")
        return categoria
        
    def clean_activa(self):
        activa = self.cleaned_data.get("activa")
        return activa
        
    