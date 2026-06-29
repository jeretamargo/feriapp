from django import forms
from ..models import Categoria


class FeriaFilterForm(forms.Form):
    nombre = forms.CharField(required=False, label="Nombre")
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False, label="Categoría")
    fecha_inicio_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="Fecha inicio desde")
    fecha_inicio_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}), label="Fecha inicio hasta")
    ubicacion = forms.CharField(required=False, label="Ubicación")
    activa = forms.ChoiceField(
        required=False,
        choices=(("", "Cualquiera"), ("true", "Activa"), ("false", "Inactiva")),
        label="Estado",
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre:
            return nombre.strip()
        return nombre
