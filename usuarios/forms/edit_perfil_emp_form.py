from django import forms
from django.forms import ModelForm

from usuarios.models.emprendedor_models import Emprendedor
class EmprendedorUpdateForm(ModelForm):
    class Meta:
        model = Emprendedor
        fields = [
            "nombre",
            "apellido",
            "telefono",
            "rubro"
        ]

    nombre = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            
        }
    ))
    apellido = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            
        }
    ))
    telefono = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            
        }
    ))
    rubro = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control ",
            
        }
    ))

    def clean_nombre(self):
       nombre = self.cleaned_data.get("nombre")
       if nombre and len(nombre.strip()) <= 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
       return nombre.strip()
    
    def clean_apellido(self):
       apellido = self.cleaned_data.get("apellido")
       if apellido and len(apellido.strip()) <= 3:
            raise forms.ValidationError("El apellido debe tener al menos 3 caracteres.")
       return apellido.strip()
    
    def clean_rubro(self):
       rubro = self.cleaned_data.get("rubro")
       if not rubro or not rubro.strip():
            raise forms.ValidationError("El rubro es obligatorio")
       return rubro.strip()
    
    def clean_telefono(self):
       telefono = self.cleaned_data.get("telefono")
       if not telefono or not telefono.strip():
            raise forms.ValidationError("El rubro es obligatorio")
       return telefono.strip()
    
    def save(self, commit=True):
        emprendedor = self.instance

        errores = emprendedor.update(
            nombre=self.cleaned_data["nombre"],
            apellido=self.cleaned_data["apellido"],
            rubro=self.cleaned_data["rubro"],
            telefono=self.cleaned_data["telefono"],
        )

        if errores:
            for error in errores:
                self.add_error(None, error)

        return emprendedor