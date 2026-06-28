from django import forms
from ..models import Feria
from django.utils import timezone


class FeriaAdminForm(forms.ModelForm):
    class Meta:
        model = Feria
        fields = "__all__"
        labels = {
            "nombre": "Nombre de la feria",
            "categoria": "Categoría de la feria",
            "fecha_inicio": "Fecha de inicio",
            "fecha_fin": "Fecha de finalización",
            "ubicación": "Ubicación de la feria",
            "capacidad_puestos": "Capacidad Total de Puestos"

        }
        widgets = {
        "nombre": forms.TextInput(
            attrs={
                "placeholder": "Feria del sur"
            }
        ),
        "categoria" : forms.Select(
            attrs={
               
                "class" : "form-select"
            
            }
        ),
        "fecha_inicio": forms.DateInput(
            attrs={
               
                "type": "date"
            }
        ),
        "fecha_fin": forms.DateInput(
            attrs={
               
                "type": "date"
            }
        ),
        "capacidad_puestos": forms.NumberInput(
            attrs={
                "placeholder": "80"
            }
        ),
        "ubicacion": forms.TextInput(
            attrs={
                "placeholder": "Ushuaia"
            }
        ),

    }
    def clean(self):
        cleaned_data = super().clean()

        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise forms.ValidationError(
                    "La fecha de finalización debe ser posterior a la fecha de inicio."
                )

        return cleaned_data