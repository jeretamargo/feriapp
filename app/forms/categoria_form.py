
from django import forms
from ..models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"  , "placeholder": "Nombre de la feria", "required": True}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Descripción de la feria", "required": False}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if nombre and len(nombre.strip()) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre.strip()

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion")
        if descripcion:
            return descripcion.strip()
        return ""
    
    

