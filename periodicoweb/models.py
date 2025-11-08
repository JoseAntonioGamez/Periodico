from django.db import models

# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre completo")
    bio = models.TextField(blank=True)
    edad = models.PositiveIntegerField(default=18, null=True)
    sueldo = models.DecimalField(max_digits=7, decimal_places=2, default=1200.00)
    es_redactor = models.BooleanField(default=True, editable=False)

class PerfilAutor(models.Model):
    autor = models.OneToOneField(Autor, on_delete=models.CASCADE)
    ciudad = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=15, help_text="Solo números")
    fecha_nacimiento = models.DateField(null=True, auto_now_add=True)
    hora_favorita = models.TimeField(auto_now=True)

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    registrado_en = models.DateTimeField(auto_now_add=True)
    es_premium = models.BooleanField(default=False)
    puntos = models.IntegerField(default=0, editable=True)

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    preferencia_hora = models.TimeField(auto_now=True)

class Seccion(models.Model):
    nombre = models.CharField(max_length=50, choices=[('POL', 'Política'), ('DEP', 'Deportes'), ('CUT', 'Cultura')])
    descripcion = models.TextField(blank=True)
    importancia = models.IntegerField(default=1)
    activa = models.BooleanField(default=True)

class Articulo(models.Model):
    titulo = models.CharField(max_length=150, unique=True)
    contenido = models.TextField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.SET_NULL, null=True)
    visitas = models.PositiveIntegerField(default=0)
    publicado_en = models.DateTimeField(auto_now_add=True)

class Portada(models.Model):
    articulo_principal = models.OneToOneField(Articulo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    mensaje = models.CharField(max_length=100)
    destacado = models.BooleanField(default=False)

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=30, blank=True)
    color = models.CharField(max_length=20, help_text="Color HTML")
    descripcion = models.TextField(blank=True, help_text="Descripción opcional")
    activa = models.BooleanField(default=True)

class ArticuloEtiqueta(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='articulo_etiquetas')
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)
    relevancia = models.FloatField(default=1.0)
    fecha_asignacion = models.DateField(null=True)
    comentario = models.TextField(blank=True)

class Evento(models.Model):
    nombre = models.CharField(max_length=80)
    lugar = models.CharField(max_length=50, blank=True)
    fecha = models.DateField()
    articulos = models.ManyToManyField(Articulo, blank=True) 
    capacidad = models.PositiveIntegerField(default=50)

class Grupo(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    usuarios = models.ManyToManyField(Usuario, blank=True)
    creado_en = models.DateField(auto_now_add=True)

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)  
    texto = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now=True)
    puntuacion = models.FloatField(default=0.0)
