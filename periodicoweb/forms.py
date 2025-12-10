from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    roles = (
        (UsuarioSesion.AUTOR, 'Autor'),
        (UsuarioSesion.USUARIO, 'Usuario'),
    )
    rol = forms.ChoiceField(choices=roles)

    ciudad = forms.CharField(required=False, max_length=50, label="Ciudad (solo autores)")
    telefono = forms.CharField(required=False, max_length=15, label="Teléfono (solo usuarios)")

    class Meta:
        model = UsuarioSesion
        fields = ['username', 'email', 'password1', 'password2', 'rol', 'ciudad', 'telefono']

    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        ciudad = cleaned_data.get('ciudad')
        telefono = cleaned_data.get('telefono')

        if rol == str(UsuarioSesion.AUTOR) and not ciudad:
            self.add_error('ciudad', 'La ciudad es obligatoria para autores.')

        if rol == str(UsuarioSesion.USUARIO) and not telefono:
            self.add_error('telefono', 'El teléfono es obligatorio para usuarios.')

        return cleaned_data
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

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request is not None and request.user.is_authenticated:
            if request.user.rol == UsuarioSesion.AUTOR:
                self.fields['articulos'].queryset = Articulo.objects.filter(
                    autor__usuariosesion=request.user
                )
            else:
                self.fields['articulos'].queryset = Articulo.objects.all()

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
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion and len(descripcion) > 200:
            self.add_error('descripcion', 'La descripción no puede superar 200 caracteres.')
        return descripcion
    
class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'es_premium', 'puntos']
        labels = {
            'nombre': 'Nombre del usuario',
            'es_premium': 'Usuario Premium',
            'puntos': 'Puntos acumulados',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'es_premium': forms.CheckboxInput(),
            'puntos': forms.NumberInput(),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            qs = Usuario.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('nombre', 'Ya existe un usuario con ese nombre.')
            if len(nombre) > 100:
                self.add_error('nombre', 'El nombre no puede superar 100 caracteres.')
        return nombre

    def clean_puntos(self):
        puntos = self.cleaned_data.get('puntos')
        if puntos is not None and puntos < 0:
            self.add_error('puntos', 'Los puntos no pueden ser negativos.')
        return puntos
    
class EtiquetaForm(ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre', 'color', 'descripcion', 'activa']
        labels = {
            'nombre': 'Nombre de la etiqueta',
            'color': 'Color HTML',
            'descripcion': 'Descripción',
            'activa': 'Etiqueta activa',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'color': forms.TextInput(),
            'descripcion': forms.Textarea(),
            'activa': forms.CheckboxInput(),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and len(nombre) > 30:
            self.add_error('nombre', 'El nombre no puede superar 30 caracteres.')
        return nombre

    def clean_color(self):
        color = self.cleaned_data.get('color')
        if not color:
            self.add_error('color', 'El color es obligatorio.')
        elif len(color) > 20:
            self.add_error('color', 'El color no puede superar 20 caracteres.')
        return color
    
class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['usuario', 'articulo', 'texto', 'puntuacion']
        labels = {
            'usuario': 'Usuario',
            'articulo': 'Artículo',
            'texto': 'Comentario',
            'puntuacion': 'Puntuación (0.0 - 5.0)',
        }
        widgets = {
            'usuario': forms.Select(),
            'articulo': forms.Select(),
            'texto': forms.Textarea(),
            'puntuacion': forms.NumberInput(),
        }

    def clean_texto(self):
        texto = self.cleaned_data.get('texto')
        if not texto or len(texto) < 5:
            self.add_error('texto', 'El comentario debe tener al menos 5 caracteres.')
        elif len(texto) > 500:
            self.add_error('texto', 'El comentario no puede superar 500 caracteres.')
        return texto

    def clean_puntuacion(self):
        puntuacion = self.cleaned_data.get('puntuacion')
        if puntuacion is None or not (0.0 <= puntuacion <= 5.0):
            self.add_error('puntuacion', 'La puntuación debe ser un valor entre 0.0 y 5.0.')
        return puntuacion