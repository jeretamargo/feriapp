
from app.models.resena_models import Resena
from django import forms

#añadido para ver los emprendedores segun la feria, asi deja buscar 
class ResenaForm(forms.ModelForm):


    class Meta:
        model = Resena
        fields = [        
            "emprendedor",
            "puntuacion",
            "comentario"
        ]