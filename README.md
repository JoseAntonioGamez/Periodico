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

**(nombre: estadisticas_articulos (URL6) [estadisticas_articulos.html])**

Muestra estadísticas agregadas sobre los artículos, incluyendo la longitud del contenido.

*Requisitos cumplidos:*  
- Uso combinado de annotate() y aggregate() para generar estadísticas desde la base de datos.  
- Uso de la función Length() de django.db.models.functions para calcular la longitud del campo contenido.  
- Cálculo de Count, Avg, Max y Min a partir de esa longitud.  
- Consulta SQL equivalente comentada en la vista.  
- Visualización en plantilla con formato legible y redondeo de decimales.  
- Integración en el índice principal para facilitar pruebas.

**(nombre: estadisticas_autores (URL7) [estadisticas_autores.html])**

Muestra estadísticas agrupadas por autor, incluyendo el número total de artículos publicados y la fecha del más reciente.

*Requisitos cumplidos:*  
- Uso de annotate() para realizar agregaciones agrupadas.  
- Agrupación por autor mediante values('autor__nombre').  
- Cálculo de Count() y Max() sobre los artículos asociados a cada autor.  
- Consulta SQL equivalente comentada.  
- Ordenación descendente por número de artículos. 
- Manejo de casos sin datos con bloque empty.  
- Integración en el índice principal para facilitar pruebas.

**(nombre: estadisticas_secciones (URL8) [estadisticas_secciones.html])**

Muestra estadísticas agrupadas por sección.

*Requisitos cumplidos:*  
- Uso de annotate() para agrupar por sección.  
- Cálculo de Count para total de artículos por sección.  
- Cálculo de Avg sobre la longitud del contenido de los artículos.  
- Uso de la función Length para medir longitud del contenido.  
- Orden descendente por total de artículos.  
- Manejo de casos sin datos con mensaje informativo.  
- Integración en el índice principal para facilitar pruebas.

**(nombre: ultimos_articulos (URL9) [ultimos_articulos.html])**

Muestra los últimos 5 artículos ordenados por fecha de publicación de forma descendente.

*Requisitos cumplidos:*  
- Uso de parámetro n/a, consulta directa sin parámetros.  
- Optimización con select_related para obtener datos relacionados (autor y sección).  
- Uso de order_by y limit para obtener solo los últimos 5 registros.
- Integración en el índice principal para facilitar pruebas.

**(nombre: articulos_con_etiquetas (URL10) [articulos_con_etiquetas.html])**

Muestra los artículos que tienen etiquetas asociadas mediante su relación ManyToMany.

*Requisitos cumplidos:*  
- Uso de prefetch_related para optimizar la carga de la relación ManyToMany.  
- Acceso a las etiquetas relacionadas mediante articuloetiqueta_set.  
- Combinación de select_related para traer autor y sección (ManyToOne).  
- Filtro con isnull=False para mostrar solo los artículos con etiquetas.
- Uso de order_by() y distinct() para mejorar desempeño y evitar duplicados.  
- Integración en el índice principal para facilitar pruebas.
