from django.shortcuts import render, get_object_or_404
from .models import Articulo, Seccion
from django.db.models import Q, Avg, Count, Max, Min
from django.db.models.functions import Length

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

"""
URL 4: Muestra los articulos filtrando por el nombre de la sección.
"""

def articulos_por_seccion(request, nombre):

    """
    -SQL-

    articulos = (Articulo.objects.raw(SELECT a.*
    + FROM periodicoweb_articulo a
    + INNER JOIN periodicoweb_seccion s ON a.seccion_id = s.id
    + WHERE s.nombre = '<nombre>'
    + ORDER BY a.publicado_en DESC)
    )
    """
    articulos = Articulo.objects.select_related('seccion', 'autor') \
        .filter(seccion__nombre=nombre) \
        .order_by('-publicado_en')

    return render(request, 'articulos/articulos_por_seccion.html', {'articulos': articulos, 'nombre': nombre})

"""
URL 5: Muestra los articulos que su titulo o contenido tenga el texto indicado.
"""

def buscar_articulos(request, criterio):
    """
    -SQL-

    articulos = (Articulo.objects.raw(SELECT a.*
    + FROM periodicoweb_articulo a
    + WHERE a.titulo LIKE '%<criterio>%'
    + OR a.contenido LIKE '%<criterio>%'
    + ORDER BY a.publicado_en DESC)
    )
    """
    
    articulos = Articulo.objects.select_related('autor', 'seccion') \
        .filter(Q(titulo__icontains=criterio) | Q(contenido__icontains=criterio)) \
        .order_by('-publicado_en')
    
    return render(request, 'articulos/buscar_articulos.html', {'articulos': articulos, 'criterio': criterio})

"""
URL 6: Calcula estadisticas sobre los articulos publicados, como la cantidad total, promedio, máximo y mínimo de longitud de contenido.
"""

def estadisticas_articulos(request):
    """
    -SQL-

    articulos = (Articulo.objects.raw(SELECT 
    + COUNT(*) AS total_articulos,
    + AVG(LENGTH(contenido)) AS promedio_longitud,
    + MAX(LENGTH(contenido)) AS max_longitud,
    + MIN(LENGTH(contenido)) AS min_longitud
    + FROM periodicoweb_articulo)
    )
    """
    articulos = Articulo.objects.annotate(longitud=Length('contenido'))
    estadisticas = articulos.aggregate(
        total_articulos=Count('id'),
        promedio_longitud=Avg('longitud'),
        max_longitud=Max('longitud'),
        min_longitud=Min('longitud')
    )

    return render(request, 'articulos/estadisticas_articulos.html', {'estadisticas': estadisticas})

"""
URL 7: Muestra las estadisticas de articulos agrupadas por autor.
"""

def estadisticas_autores(request):
    """
    -SQL-

    articulos = (SELECT autor_id,
    + COUNT(*) AS total_articulos,
    + MAX(publicado_en) AS ultima_publicacion
    + FROM periodicoweb_articulo
    + GROUP BY autor_id
    + ORDER BY total_articulos DESC)
    )
    """
    
    autores = (
        Articulo.objects.values('autor__nombre')
        .annotate(total_articulos=Count('id'), ultima_publicacion=Max('publicado_en'))
        .order_by('-total_articulos')
    )

    return render(request, 'articulos/estadisticas_autores.html', {'autores': autores})

"""
URL 8: Muestra estadísticas por sección, usando annotate para el calculo total de articulos y promedio de longitud del contenido de artículos para cada sección.
"""

def estadisticas_secciones(request):
    """
    -SQL-

    articulos = (Articulo.objects.raw(SELECT s.nombre,
    + COUNT(a.id) AS total_articulos,
    + AVG(LENGTH(a.contenido)) AS promedio_longitud
    + FROM periodicoweb_seccion s
    + LEFT JOIN periodicoweb_articulo a ON a.seccion_id = s.id
    + GROUP BY s.nombre
    + ORDER BY total_articulos DESC)
    )
    """
    
    secciones = Seccion.objects.annotate(
        total_articulos=Count('articulo'),
        promedio_longitud=Avg(Length('articulo__contenido'))
    ).order_by('-total_articulos')

    return render(request, 'articulos/estadisticas_secciones.html', {'secciones': secciones})

"""
URL 9: Muestra los útimos 5 artículos por fecha de publicación descendente, incluyendo datos de autor y sección.
"""

def ultimos_articulos(request):
    """
    -SQL-

    articulos = (Articulo.objects.raw(SELECT a.*, au.nombre AS autor_nombre, s.nombre AS seccion_nombre
    FROM periodicoweb_articulo a
    LEFT JOIN periodicoweb_autor au ON a.autor_id = au.id
    LEFT JOIN periodicoweb_seccion s ON a.seccion_id = s.id
    ORDER BY a.publicado_en DESC
    LIMIT 5)
    )
    """
    
    articulos = Articulo.objects.select_related('autor', 'seccion').order_by('-publicado_en')[:5]

    return render(request, 'articulos/ultimos_articulos.html', {'articulos': articulos})