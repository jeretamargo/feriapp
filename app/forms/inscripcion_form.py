from django import forms
from app.models.inscripcion_models import Inscripcion
from app.models.feria_models import Feria


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ["feria"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # solo mostrar ferias activas y con lugar disponible
        self.fields["feria"].queryset = Feria.objects.filter(activa=True)
        self.fields["feria"].label = "Feria"