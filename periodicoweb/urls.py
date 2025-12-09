from django.urls import path, re_path
from .import views

urlpatterns = [
    path('', views.index, name='index'),

    path('registrar', views.registrar_usuario, name='registrar_usuario'),
    path('logout/', views.logout_view, name='logout'),

    path('autores/', views.autor_list, name='autor_list'),
    path('autores/nuevo/', views.autor_create, name='autor_create'),
    path('autores/<int:pk>/editar/', views.autor_update, name='autor_update'),
    path('autores/<int:pk>/eliminar/', views.autor_delete, name='autor_delete'),

    path('eventos/', views.evento_list, name='evento_list'),
    path('eventos/nuevo/', views.evento_create, name='evento_create'),
    path('eventos/<int:pk>/editar/', views.evento_update, name='evento_update'),
    path('eventos/<int:pk>/eliminar/', views.evento_delete, name='evento_delete'),

    path('grupos/', views.grupo_list, name='grupo_list'),
    path('grupos/nuevo/', views.grupo_create, name='grupo_create'),
    path('grupos/<int:pk>/editar/', views.grupo_update, name='grupo_update'),
    path('grupos/<int:pk>/eliminar/', views.grupo_delete, name='grupo_delete'),

    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/nuevo/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', views.usuario_delete, name='usuario_delete'),

    path('etiquetas/', views.etiqueta_list, name='etiqueta_list'),
    path('etiquetas/nuevo/', views.etiqueta_create, name='etiqueta_create'),
    path('etiquetas/<int:pk>/editar/', views.etiqueta_update, name='etiqueta_update'),
    path('etiquetas/<int:pk>/eliminar/', views.etiqueta_delete, name='etiqueta_delete'),

    path('comentarios/', views.comentario_list, name='comentario_list'),
    path('comentarios/nuevo/', views.comentario_create, name='comentario_create'),
    path('comentarios/<int:pk>/editar/', views.comentario_update, name='comentario_update'),
    path('comentarios/<int:pk>/eliminar/', views.comentario_delete, name='comentario_delete'),
]