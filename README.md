# Periódico - Documentación

## Explicación de URLs y Requisitos Cumplidos

**(nombre: index [index.html])**  

Renderiza la página principal índice con enlaces a otras URLs del proyecto.  

*Requisitos cumplidos:*  
- Proporciona una página de inicio con navegación básica.

**(nombre: lista_articulos (URL1) [articulos.html])**  

Muestra los artículos con su autor, sección (si tiene, por ello el else) y fecha de publicación.  

*Requisitos cumplidos:*  
- Traer datos relacionados en una sola consulta para mejorar el rendimiento.  
- Mostrar los artículos ordeandos por fecha de forma descendente.  
- Mostrar un mensaje si no hay artículos disponibles.

**(nombre: detalle_articulo (URL2) [detalle.html])**  

Muestra toda la información del artículo seleccionado por ID, incluyendo datos relacionados.

*Requisitos cumplidos:*  
- URL con parámetro entero.  
- Relación ManyToOne con autor y sección obtenida con select_related (consulta optimizada).  
- Consulta SQL comentada en el código.  
- Vista y plantilla muestran todo el detalle solicitado.  
- Manejo de error 404 con get_object_or_404. 

**(nombre: articulos_por_fecha (URL3) [articulos_por_fecha.html])**  

Lista artículos publicados en un año y mes determinados.

*Requisitos cumplidos:*  
- URL con dos parámetros enteros.  
- Uso de filtros AND en QuerySet para extraer los artículos de esa fecha.  
- Select_related para optimizar las relaciones ManyToOne.  
- Consulta SQL equivalente comentada.  
- Ordena los artículos por fecha descendente.  
- Muestra toda la información relacionada de autor y sección. 

**(nombre: articulos_por_seccion (URL4) [articulos_por_seccion.html])**  

Lista artículos filtrados por abreviatura corta (campo nombre) de la sección, usando expresión regular en la URL (re_path).

*Requisitos cumplidos:*  
- Uso de re_path para la URL con expresión regular y parámetro string en nombre.  
- Filtro string válido en relación ManyToOne: seccion__nombre=nombre.  
- Optimización con select_related para incluir datos de autor y sección en la consulta.  
- Consulta SQL equivalente comentada.

**(nombre: buscar_articulos (URL5) [buscar_articulos.html])**

Busca artículos cuyo título o contenido contengan un texto determinado (parámetro string). Usa filtros combinados con OR mediante objetos Q.

*Requisitos cumplidos:*
- Uso de parámetro string en la URL.
- Filtro OR mediante Q objects.
- Relación ManyToOne (autor, sección) optimizada con select_related.
- Consulta SQL equivalente comentada en la vista.
- Orden descendente por fecha de publicación.
- Página funcional mostrando título, autor, sección y fecha.
- Manejo de casos donde no se encuentran resultados.
- Integración en el índice principal para facilitar pruebas.