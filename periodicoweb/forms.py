from django import forms
from django.core.exceptions import ValidationError
from .models import *

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'bio', 'edad', 'sueldo', 'es_redactor']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 18
            }),
            'sueldo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            # editable=False en el modelo, solo se muestra como checkbox deshabilitado
            'es_redactor': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'disabled': True,
            }),
        }

    # Validación 1: nombre único “bonita”, además de unique=True en modelo
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Si es actualización, evita chocar consigo mismo
        instancia = getattr(self, 'instance', None)
        qs = Autor.objects.filter(nombre__iexact=nombre)
        if instancia and instancia.pk:
            qs = qs.exclude(pk=instancia.pk)
        if qs.exists():
            raise ValidationError("Ya existe un autor con ese nombre.")
        return nombre

    # Validación 2: edad mínima 18
    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad is not None and edad < 18:
            raise ValidationError("La edad mínima es 18 años.")
        return edad

