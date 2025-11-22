# app/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Asistencia


def solo_letras_validator(value):
    if not value.replace(" ", "").isalpha():
        raise ValidationError("Solo se permiten letras y espacios")


class AsistenciaForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=50,
        min_length=2,
        validators=[solo_letras_validator],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej: Ricardo",
                "class": "w-full bg-slate-800 border border-slate-500 rounded-lg px-3 py-2.5 text-sm text-slate-50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400",
                "required": True,
            }
        ),
    )

    apellido = forms.CharField(
        max_length=50,
        min_length=2,
        validators=[solo_letras_validator],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej: Salazar",
                "class": "w-full bg-slate-800 border border-slate-500 rounded-lg px-3 py-2.5 text-sm text-slate-50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400",
                "required": True,
            }
        ),
    )

    curso = forms.CharField(
        max_length=50,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej: 5to nivel B1",
                "class": "w-full bg-slate-800 border border-slate-500 rounded-lg px-3 py-2.5 text-sm text-slate-50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400",
                "required": True,
            }
        ),
    )

    materia = forms.CharField(
        max_length=80,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej: Construcción de Software",
                "class": "w-full bg-slate-800 border border-slate-500 rounded-lg px-3 py-2.5 text-sm text-slate-50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400",
                "required": True,
            }
        ),
    )

    class Meta:
        model = Asistencia
        fields = ["nombre", "apellido", "curso", "materia"]
