from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import *

class AutorForm(ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'bio', 'edad', 'sueldo', 'es_redactor', 'foto']
        labels = {
            'nombre': 'Nombre completo del autor',
            'bio': 'Biografía',
            'edad': 'Edad',
            'sueldo': 'Sueldo mensual (€)',
            'es_redactor': 'Es redactor',
            'foto': 'Foto del autor',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'bio': forms.Textarea(),
            'edad': forms.NumberInput(),
            'sueldo': forms.NumberInput(),
            'es_redactor': forms.CheckboxInput(),
            'foto': forms.ClearableFileInput(),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not nombre:
            return nombre

        if len(nombre) > 100:
            self.add_error('nombre', 'El nombre no puede superar 100 caracteres.')

        qs = Autor.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            self.add_error('nombre', 'Ya existe un autor con ese nombre.')

        return nombre

    def clean_sueldo(self):
        sueldo = self.cleaned_data.get('sueldo')

        if sueldo is None:
            self.add_error('sueldo', 'Introduce un sueldo válido (número).')

        return sueldo

    def clean(self):
        cleaned_data = super().clean()

        edad = cleaned_data.get('edad')
        sueldo = cleaned_data.get('sueldo')

        if edad is not None and edad < 18:
            self.add_error('edad', 'La edad mínima es 18 años.')

        if edad is not None and sueldo is not None:
            if edad > 65 and sueldo < 1000:
                self.add_error('edad', 'Para autores mayores de 65 años se espera un sueldo mínimo de 1000€.')
                self.add_error('sueldo', 'Revisa el sueldo para autores mayores de 65 años.')

        return cleaned_data
    
class EventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'lugar', 'fecha', 'articulos', 'capacidad']
        labels = {
            'nombre': 'Nombre del evento',
            'lugar': 'Lugar',
            'fecha': 'Fecha del evento',
            'articulos': 'Artículos relacionados',
            'capacidad': 'Capacidad',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'lugar': forms.TextInput(),
            'fecha': forms.DateInput(),
            'articulos': forms.SelectMultiple(),
            'capacidad': forms.NumberInput(),
        }


    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            qs = Evento.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('nombre', 'Ya existe un evento con ese nombre.')
            if len(nombre) > 80:
                self.add_error('nombre', 'El nombre no puede superar 80 caracteres.')
        return nombre


    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad is not None and capacidad < 1:
            self.add_error('capacidad', 'La capacidad debe ser un número mayor o igual a 1.')
        return capacidad

class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'descripcion', 'usuarios']
        labels = {
            'nombre': 'Nombre del grupo',
            'descripcion': 'Descripción',
            'usuarios': 'Usuarios asociados',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'descripcion': forms.Textarea(),
            'usuarios': forms.SelectMultiple(),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            qs = Grupo.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('nombre', 'Ya existe un grupo con ese nombre.')
            if len(nombre) > 80:
                self.add_error('nombre', 'El nombre no puede superar 80 caracteres.')
        return nombre