from django.urls import path, re_path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articulos/', views.listar_articulos, name='lista_articulos'),
    path('articulo/<int:id>/', views.detalle_articulo, name='detalle_articulo'),
    path('articulos/fecha/<int:anio>/<int:mes>/', views.articulos_por_fecha, name='articulos_por_fecha'),
    re_path(r'^articulos/seccion/(?P<nombre>[\w-]+)/$', views.articulos_por_seccion, name='articulos_por_seccion'),
    path('articulos/busqueda/<str:criterio>/', views.buscar_articulos, name='buscar_articulos'),
    path('articulos/estadisticas/', views.estadisticas_articulos, name='estadisticas_articulos'),
    path('autores/estadisticas/', views.estadisticas_autores, name='estadisticas_autores'),
    path('secciones/estadisticas/', views.estadisticas_secciones, name='estadisticas_secciones'),
    path('ultimos_articulos/', views.ultimos_articulos, name='ultimos_articulos'),
    path('articulos/con_etiquetas/', views.articulos_con_etiquetas, name='articulos_con_etiquetas'),

    path('autores/', views.autor_list, name='autor_list'),
    path('autores/nuevo/', views.autor_create, name='autor_create'),
    path('autores/<int:pk>/editar/', views.autor_update, name='autor_update'),
    path('autores/<int:pk>/eliminar/', views.autor_delete, name='autor_delete'),

    path('eventos/', views.evento_list, name='evento_list'),
    path('eventos/nuevo/', views.evento_create, name='evento_create'),
    path('eventos/<int:pk>/editar/', views.evento_update, name='evento_update'),
    path('eventos/<int:pk>/eliminar/', views.evento_delete, name='evento_delete'),
]