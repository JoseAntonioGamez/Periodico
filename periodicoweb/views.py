from django.shortcuts import render
from .models import Articulo

# Create your views here.
def post_list(request):
    return render(request, 'periodico/post_list.html', {})

"""
Página índice estática con enlaces a otras urls
"""
def index(request):
    return render(request, 'index.html')

"""
URL 1: Obtiene todos los articulos junto con su autor y seccion asociados.
"""
def listar_articulos(request):
    articulos = Articulo.objects.select_related('autor', 'seccion').all().order_by('-publicado_en')

    """
    -SQL-

    articulos = (Articulo.objects.raw("SELECT a.* FROM periodicoweb_articulo a "
    + "JOIN periodicoweb_autor au ON a.autor_id = au.id "
    + "LEFT JOIN periodicoweb_seccion s ON a.seccion_id = s.id "
    + "ORDER BY a.publicado_en DESC")
    )

    """
    return render(request, 'articulos/articulos.html', {'articulos': articulos})