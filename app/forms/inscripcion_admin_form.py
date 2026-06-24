from django import forms

from usuarios.models.user_models import User
from ..models import Inscripcion
from django.utils import timezone


class InscripcionAdminForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = "__all__"
        labels = {
            "emprendedor": "Emprendedor a inscribir",
            "feria": "Feria a la que se inscribe",
            "numero_puesto": "Numero de puesto",
            "fecha_inscripcion": "Fecha de inscripción",
            "estado": "Estado de la inscripción",
            "registrado_por": "Administrador responsable"

        }
        widgets = {
        "emprendedor": forms.Select(
           
        ),
        "feria" : forms.Select(
            attrs={
               
                "class" : "form-select"
            
            }
        ),
        "numero_puesto": forms.NumberInput(
            attrs={
                "placeholder": "1",
                "type": "date"
            }
        ),
        "fecha_inscripcion": forms.DateInput(
            attrs={
                
                "type": "date"
            }
        ),
        "capacidad_puestos": forms.Select(
            attrs={
                "placeholder": "En Espera"
            }
        ),
        "registrado_por": forms.Select(
            attrs={
                
                "class" : "form-select"
            }
        ),

    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["registrado_por"].queryset = User.objects.filter(
            is_superuser=True
        )