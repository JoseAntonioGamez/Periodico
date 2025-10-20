from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articulos/', views.listar_articulos, name='lista_articulos'),
]
