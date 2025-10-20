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
