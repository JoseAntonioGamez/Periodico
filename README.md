# Proyecto Periódico Web - Requisitos cumplidos y su implementación

Este documento detalla todos los requisitos funcionales y técnicos que se han cumplido en el proyecto, indicando los archivos implicados y el comportamiento concreto que implementan.

## 1. Menú de navegación superior con enlaces
- **Archivo:** `navbar.html`
- **Uso:** Incluido en `base.html` con `{% include 'navbar.html' %}`
- **Función:** 
  - Ofrece navegación común en todas las páginas.
  - Mejora la usabilidad y facilita la exploración del sitio.

## 2. Pie de página de la web
- **Archivo:** `footer.html`
- **Uso:** Incluido en `base.html` con `{% include 'footer.html' %}`
- **Función:**
  - Proporciona información de copyright consistente.
  - Presente en todas las páginas para uniformidad.

## 3. Plantilla base incluyendo menú y pie, con bloques especializados
- **Archivo:** `base.html`
- **Uso:** Extendida por todas las demás plantillas con `{% extends 'base.html' %}`
- **Bloques:** 
  - `header`: Para títulos o cabeceras específicas de cada página.
  - `content`: Para el contenido variable principal.
- **Función:** 
  - Centraliza y unifica la estructura común, garantizando coherencia.
  - Facilita modularidad y mantenimiento.

## 4. Inclusión de CSS, JavaScript y logotipo
- **Dónde:** Cargados en el `<head>` de `base.html` usando `{% load static %}` y la etiqueta `{% static '...' %}`
- **Imagen:** Logo insertado con etiqueta `<img src="{% static 'img/logo.png' %}" ...>` en el `header`.
- **Función:**
  - Estiliza el sitio con CSS responsive.
  - Añade funcionalidades básicas con JavaScript.
  - Refuerza la identidad visual del portal.

## 5. Herencia de todas las páginas desde la plantilla base
- **Cómo:** Todas las plantillas hijas utilizan `{% extends "base.html" %}`
- **Función:** Unifica diseño, comportamiento y estructura de toda la web.

## 6. Refactorización del bucle `for` en inclusiones parciales
- **Ejemplo:** Listas de artículos usan `{% include "articulos/articulo_item.html" %}` para los items.
- **Función:** Mejor mantenimiento, evita duplicación y facilita actualizaciones.

---

# Uso de Template Filters

| Filtro        | Función                                     | Uso concreto                   |
|---------------|--------------------------------------------|-------------------------------|
| `date`        | Formato de fechas legible                   | Fechas de publicación          |
| `floatformat` | Redondeo y formato numérico                 | Estadísticas con decimales     |
| `truncatewords` | Resumen de texto a X palabras             | Previews de artículos          |
| `capfirst`    | Primer letra en mayúscula                    | Títulos y nombres              |
| `upper`       | Texto en mayúsculas                          | Nombres de autor               |
| `default_if_none` | Valor por defecto si dato nulo            | Secciones sin nombre           |
| `linebreaks`  | Convierte saltos de línea en etiquetas HTML | Contenido de artículos formateado |
| `length`      | Conteo de elementos o caracteres             | Longitudes y totales en estadísticas |
| `lower`       | Texto en minúsculas                          | Etiquetas y criterios de búsqueda |
| `intcomma`    | Separador de miles en números grandes        | Estadísticas numéricas (requiere `humanize`)  |

# Uso de Template Tags

| Tag           | Función                                      | Ejemplo concreto               |
|---------------|---------------------------------------------|-------------------------------|
| `{% if %}`    | Condicionales para mostrar contenido         | Manejo de valores nulos, filtros de sección |
| `{% else %}`  | Alternativa en condicional                    | Combina con `{% if %}`          |
| `{% for %}`   | Iteración sobre colecciones                   | Listado de artículos            |
| `{% empty %}` | Mensaje cuando listas están vacías            | Gestión de listas sin resultados|
| `{% include %}` | Reutilización de fragmentos                   | Inclusión de `articulo_item.html` para modularización |
| `{% extends %}` | Hereda plantilla base                         | Todas las vistas con diseño común |
| `{% load %}`  | Carga librerías de filtros o tags             | Carga de `static` y `humanize`  |

## Operadores usados en `{% if %}`

| Operador | Función                       | Ejemplo                       |
|----------|------------------------------|-------------------------------|
| `==`     | Igualdad                     | `{% if seccion == "DEP" %}`    |
| `!=`     | Desigualdad                  | `{% if nombre != None %}`      |
| `<`      | Menor que                   | `{% if contador < 10 %}`       |
| `>`      | Mayor que                   | `{% if longitud > 100 %}`      |
| `not`    | Negación                    | `{% if not articulo.seccion %}` |


