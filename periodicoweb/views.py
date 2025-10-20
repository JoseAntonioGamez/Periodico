from django.shortcuts import render, get_object_or_404
from .models import Articulo
from django.db.models import Q

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

"""
URL 2: Muestra los detalles especificos de un articulo especifico por su ID.
"""

def detalle_articulo(request, id):
    
    """
    -SQL-

    articulos = (Articulo.objects.raw(SELECT a.*, au.nombre AS autor_nombre, s.nombre AS seccion_nombre
    + FROM periodicoweb_articulo a
    + INNER JOIN periodicoweb_autor au ON a.autor_id = au.id
    + LEFT JOIN periodicoweb_seccion s ON a.seccion_id = s.id
    + WHERE a.id = <id>)
    )
    """

    articulo = get_object_or_404(
        Articulo.objects.select_related('autor', 'seccion'),
        pk=id
    )

    return render(request, 'articulos/detalle.html', {'articulo': articulo})

"""
URL 3: Muestra los articulos publicados en un año y mes específicos.
"""

def articulos_por_fecha(request, anio, mes):
    """
    -SQL-

    articulos = (Articulo.objects.raw(SELECT a.*
    + FROM periodicoweb_articulo a
    + WHERE EXTRACT(YEAR FROM a.publicado_en) = <anio>
    + AND EXTRACT(MONTH FROM a.publicado_en) = <mes>
    + ORDER BY a.publicado_en DESC)
    )
    """

    articulos = Articulo.objects.select_related('autor', 'seccion') \
        .filter(publicado_en__year=anio, publicado_en__month=mes) \
        .order_by('-publicado_en')

    return render(request, 'articulos/articulos_por_fecha.html', {'articulos': articulos, 'anio': anio, 'mes': mes})