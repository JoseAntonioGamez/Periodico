from django.contrib import admin
from .models import Autor, PerfilAutor, Usuario, PerfilUsuario, Seccion, Articulo, Portada, Etiqueta, ArticuloEtiqueta, Evento, Grupo, Comentario

# Register your models here.

admin.site.register(Autor)
admin.site.register(PerfilAutor)
admin.site.register(Usuario)
admin.site.register(PerfilUsuario)
admin.site.register(Seccion)
admin.site.register(Articulo)
admin.site.register(Portada)
admin.site.register(Etiqueta)
admin.site.register(ArticuloEtiqueta)
admin.site.register(Evento)
admin.site.register(Grupo)
admin.site.register(Comentario)
