from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q, Avg, Count, Max, Min, Prefetch
from django.db.models.functions import Length
from django.shortcuts import render
from django.views.defaults import page_not_found
from .forms import *


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
    articulos = Articulo.objects.select_related('autor', 'seccion').order_by('-publicado_en').all()

    """
    -SQL-

    articulos = Articulo.objects.raw(
        SELECT a.* 
        FROM periodicoweb_articulo a
        JOIN periodicoweb_autor au ON a.autor_id = au.id
        LEFT JOIN periodicoweb_seccion s ON a.seccion_id = s.id
        ORDER BY a.publicado_en DESC
    )
    """

    return render(request, 'articulos/articulos.html', {'articulos': articulos})


"""
URL 2: Muestra los detalles especificos de un articulo especifico por su ID.
"""


def detalle_articulo(request, id):
    
    """
    -SQL-

    articulos = Articulo.objects.raw(
        SELECT a.*, au.nombre AS autor_nombre, s.nombre AS seccion_nombre
        FROM periodicoweb_articulo a
        INNER JOIN periodicoweb_autor au ON a.autor_id = au.id
        LEFT JOIN periodicoweb_seccion s ON a.seccion_id = s.id
        WHERE a.id = %s, [id])
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

    articulos = Articulo.objects.raw(
        SELECT a.*
        FROM periodicoweb_articulo a
        WHERE EXTRACT(YEAR FROM a.publicado_en) = %s
        AND EXTRACT(MONTH FROM a.publicado_en) = %s
        ORDER BY a.publicado_en DESC, [anio, mes])
    """

    articulos = Articulo.objects.select_related('autor', 'seccion') \
        .filter(publicado_en__year=anio, publicado_en__month=mes) \
        .order_by('-publicado_en').all()

    return render(request, 'articulos/articulos_por_fecha.html', {'articulos': articulos, 'anio': anio, 'mes': mes})


"""
URL 4: Muestra los articulos filtrando por el nombre de la sección.
"""


def articulos_por_seccion(request, nombre):


    """
    -SQL-

    articulos = Articulo.objects.raw(
        SELECT a.*
        FROM periodicoweb_articulo a
        INNER JOIN periodicoweb_seccion s ON a.seccion_id = s.id
        WHERE s.nombre = %s
        ORDER BY a.publicado_en DESC, [nombre])
    """
    articulos = Articulo.objects.select_related('seccion', 'autor') \
        .filter(seccion__nombre=nombre) \
        .order_by('-publicado_en').all()


    return render(request, 'articulos/articulos_por_seccion.html', {'articulos': articulos, 'nombre': nombre})


"""
URL 5: Muestra los articulos que su titulo o contenido tenga el texto indicado.
"""


def buscar_articulos(request, criterio):
    """
    -SQL-

    articulos = Articulo.objects.raw(
        SELECT a.*
        FROM periodicoweb_articulo a
        WHERE a.titulo LIKE %s
        OR a.contenido LIKE %s
        ORDER BY a.publicado_en DESC, 
        ['%' + criterio + '%', '%' + criterio + '%'])
    """
    
    articulos = Articulo.objects.select_related('autor', 'seccion') \
        .filter(Q(titulo__icontains=criterio) | Q(contenido__icontains=criterio)) \
        .order_by('-publicado_en').all()
    
    return render(request, 'articulos/buscar_articulos.html', {'articulos': articulos, 'criterio': criterio})


"""
URL 6: Calcula estadisticas sobre los articulos publicados, como la cantidad total, promedio, máximo y mínimo de longitud de contenido.
"""


def estadisticas_articulos(request):
    """
    -SQL-

    articulos = Articulo.objects.raw(
        SELECT 
        COUNT(*) AS total_articulos,
        AVG(LENGTH(contenido)) AS promedio_longitud,
        MAX(LENGTH(contenido)) AS max_longitud,
        MIN(LENGTH(contenido)) AS min_longitud
        FROM periodicoweb_articulo
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

    autores = Articulo.objects.raw(
        SELECT autor_id,
        COUNT(*) AS total_articulos,
        MAX(publicado_en) AS ultima_publicacion
        FROM periodicoweb_articulo
        GROUP BY autor_id
        ORDER BY total_articulos DESC
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

    secciones = Seccion.objects.raw(
        SELECT s.nombre,
        COUNT(a.id) AS total_articulos,
        AVG(LENGTH(a.contenido)) AS promedio_longitud
        FROM periodicoweb_seccion s
        LEFT JOIN periodicoweb_articulo a ON a.seccion_id = s.id
        GROUP BY s.nombre
        ORDER BY total_articulos DESC
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

    articulos = Articulo.objects.raw(
        SELECT a.*, au.nombre AS autor_nombre, s.nombre AS seccion_nombre
        FROM periodicoweb_articulo a
        LEFT JOIN periodicoweb_autor au ON a.autor_id = au.id
        LEFT JOIN periodicoweb_seccion s ON a.seccion_id = s.id
        ORDER BY a.publicado_en DESC
        LIMIT 5)
    """
    
    articulos = Articulo.objects.select_related('autor', 'seccion').order_by('-publicado_en').all()[:5]


    return render(request, 'articulos/ultimos_articulos.html', {'articulos': articulos})


"""
URL 10: Muestra los artículos que no tienen etiquetas asociadas.
"""


def articulos_con_etiquetas(request):
    """
    -SQL-

    articulos = Articulo.objects.raw(
        SELECT DISTINCT a.*
        FROM periodicoweb_articulo a
        JOIN periodicoweb_articulo_etiquetas ae ON ae.articulo_id = a.id
        JOIN periodicoweb_etiqueta e ON e.id = ae.etiqueta_id
        ORDER BY a.publicado_en DESC
    )
    """
    
    etiquetas_prefetch = Prefetch('articulo_etiquetas__etiqueta', queryset=Etiqueta.objects.all())
    articulos = (
        Articulo.objects.prefetch_related(etiquetas_prefetch)
                        .select_related('autor', 'seccion')
                        .filter(articulo_etiquetas__isnull=False)
                        .distinct()
                        .order_by('-publicado_en')[:10]
    )
    return render(request, 'articulos/articulos_con_etiquetas.html', {'articulos': articulos})

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html', None, None, 400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html', None, None, 403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', None, None, 404)

def mi_error_500(request):
    return render(request, 'errores/500.html', None, None, 500)

"""
CRUD 1: Autor
"""

def autor_list(request):
    query_nombre = request.GET.get('nombre', '').strip()
    query_edad = request.GET.get('edad', '').strip()
    query_sueldo = request.GET.get('sueldo', '').strip()

    autores = Autor.objects.all()

    if query_nombre:
        autores = autores.filter(nombre__icontains=query_nombre)

    if query_edad:
        try:
            autores = autores.filter(edad=int(query_edad))
        except ValueError:
            pass

    if query_sueldo:
        try:
            autores = autores.filter(sueldo=query_sueldo)
        except ValueError:
            pass

    autores = autores.order_by('nombre')  

    context = {
        'autores': autores,
        'query_nombre': query_nombre,
        'query_edad': query_edad,
        'query_sueldo': query_sueldo,
    }
    return render(request, 'autor/autor_list.html', context)


def autor_create(request):
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)
        if form.is_valid():
            autor = form.save()
            messages.success(request, f'Se ha creado el autor "{autor.nombre}" correctamente.')
            return redirect('autor_list')
    else:
        form = AutorForm()

    return render(request, 'autor/autor_form.html', {
        'form': form,
        'title': 'Crear autor',
    })

def autor_update(request, pk):
    autor = Autor.objects.filter(pk=pk).first()
    if not autor:
        messages.error(request, 'El autor no existe.')
        return redirect('autor_list')
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES, instance=autor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Se ha actualizado el autor "{autor.nombre}" correctamente.')
            return redirect('autor_list')
    else:
        form = AutorForm(instance=autor)

    return render(request, 'autor/autor_form.html', {
        'form': form,
        'title': 'Editar autor',
    })


def autor_delete(request, pk):
    autor = Autor.objects.filter(pk=pk).first()
    if not autor:
        messages.error(request, 'El autor no existe o ya ha sido eliminado.')
        return redirect('autor_list')

    if request.method == 'POST':
        nombre = autor.nombre
        autor.delete()
        messages.success(request, f'Se ha eliminado el autor "{nombre}".')
        return redirect('autor_list')

    return redirect('autor_list')

"""
CRUD 2: Evento
"""

def evento_list(request):
    query_nombre = request.GET.get('nombre', '').strip()
    query_lugar = request.GET.get('lugar', '').strip()
    query_fecha = request.GET.get('fecha', '').strip()

    eventos = Evento.objects.all()

    if query_nombre:
        eventos = eventos.filter(nombre__icontains=query_nombre)
    if query_lugar:
        eventos = eventos.filter(lugar__icontains=query_lugar)
    if query_fecha:
        try:
            eventos = eventos.filter(fecha=query_fecha)
        except ValueError:
            pass

    eventos = eventos.order_by('fecha', 'nombre')

    context = {
        'eventos': eventos,
        'query_nombre': query_nombre,
        'query_lugar': query_lugar,
        'query_fecha': query_fecha,
    }
    return render(request, 'evento/evento_list.html', context)

def evento_create(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()
            messages.success(request, f'Se ha creado el evento "{evento.nombre}" correctamente.')
            return redirect('evento_list')
        else:
            messages.error(request, 'Hay errores en el formulario. Revisa los campos.')
    else:
        form = EventoForm()

    return render(request, 'evento/evento_form.html', {'form': form, 'title': 'Crear evento'})

def evento_update(request, pk):
    evento = Evento.objects.filter(pk=pk).first()
    if not evento:
        messages.error(request, 'El evento no existe.')
        return redirect('evento_list')

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Se ha actualizado el evento "{evento.nombre}" correctamente.')
            return redirect('evento_list')
        else:
            messages.error(request, 'Hay errores en el formulario. Revisa los campos.')
    else:
        form = EventoForm(instance=evento)

    return render(request, 'evento/evento_form.html', {'form': form, 'title': 'Editar evento'})

def evento_delete(request, pk):
    evento = Evento.objects.filter(pk=pk).first()
    if not evento:
        messages.error(request, 'El evento no existe o ya ha sido eliminado.')
        return redirect('evento_list')

    if request.method == 'POST':
        nombre = evento.nombre
        evento.delete()
        messages.success(request, f'Se ha eliminado el evento "{nombre}".')
        return redirect('evento_list')

    return redirect('evento_list')