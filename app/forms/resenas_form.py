
from app.models.resena_models import Resena
from django import forms

#añadido para ver los emprendedores segun la feria, asi deja buscar 
class ResenaForm(forms.ModelForm):

    #varie el estilo de los botones de radio para la puntuacion, para que se vea mejor 
    puntuacion = forms.ChoiceField(
    choices=[(i, i) for i in range(1, 6)],
    widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    label="Puntuación"
    )


    class Meta:
        model = Resena
        fields = ["emprendedor", "puntuacion", "comentario"]
        widgets = {
            #para elcampo de comentario, que sea un poco mas chico
            "comentario": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Contá tu experiencia...",
                "class": "form-control"
            }),
            "puntuacion": forms.NumberInput(attrs={
                "min": 1,
                "max": 5,
                "class": "form-control"
            }),
        }