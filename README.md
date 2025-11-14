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

### Template Tags usados y archivos donde se encuentran

| Template Tag | Descripción                                  | Archivos donde se usan                                                                                         |
|--------------|----------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `extends`    | Herencia de plantilla base                    | index.html, articulos.html, detalle.html, estadisticas_articulos.html, estadisticas_autores.html, estadisticas_secciones.html, ultimos_articulos.html, articulos_por_seccion.html, articulos_por_fecha.html, buscar_articulos.html, articulos_con_etiquetas.html   |
| `block`      | Define bloques reutilizables                  | base.html (definición), todas las plantillas hijas mencionadas arriba (sobreescritura)                         |
| `include`    | Incluye fragmentos reutilizables              | base.html (navbar.html, footer.html), archivos de listas y búsqueda: articulos.html, articulos_con_etiquetas.html, articulos_por_fecha.html, articulos_por_seccion.html, buscar_articulos.html, ultimos_articulos.html           |
| `for`        | Itera sobre listas o querysets                 | articulos.html, articulos_con_etiquetas.html, articulos_por_fecha.html, articulos_por_seccion.html, buscar_articulos.html, ultimos_articulos.html, estadisticas_autores.html, estadisticas_secciones.html                      |
| `empty`      | Rama alternativa para bucles vacíos            | Artículos y búsquedas relacionados con `for`                                                                   |
| `if/else`    | Condicionales para mostrar contenido dinámico | estadisticas_autores.html, estadisticas_secciones.html, articulos.html, ultimos_articulos.html                    |
| `load`       | Importa librerías para filtros especiales      | base.html (`static`), estadisticas_articulos.html (`humanize`)                                                  |
| `url`        | Genera URLs dinámicas con nombres de ruta      | navbar.html                                                                                                     |
| `static`     | Acceso a archivos estáticos                     | base.html, navbar.html, footer.html                                                                             |

---

### Operadores `if` usados y archivos donde se emplean

| Operador | Descripción             | Archivos                                                       |
|----------|-------------------------|----------------------------------------------------------------|
| `and`    | Y lógico                | articulos.html                                                  |
| `not`    | Negación lógica         | articulos.html                                                  |
| `==`     | Igualdad                | estadisticas_autores.html                                       |
| `>`      | Mayor que               | estadisticas_autores.html                                       |
| `!=`     | Distinto de             | estadisticas_autores.html                                       |
| `or`     | O lógico (uso posible)  | Varias plantillas según @README (posible uso en búsquedas)      |

---

### Template Filters usados y archivos donde se aplican

| Filter          | Descripción                                | Archivos                                                                                                                |
|-----------------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `capfirst`      | Pone la primera letra en mayúscula         | articulo_item.html, estadisticas_secciones.html                                                                          |
| `upper`         | Convierte en mayúsculas                     | articulo_item.html                                                                                                       |
| `lower`         | Convierte en minúsculas                     | articulos_con_etiquetas.html                                                                                            |
| `default`       | Valor por defecto si campo vacío            | articulo_item.html, articulos_por_fecha.html                                                                             |
| `default_if_none`| Valor por defecto si campo es None          | articulo_item.html, articulos_por_fecha.html, articulos_por_seccion.html                                                  |
| `title`         | Capitaliza todas las palabras               | articulos_con_etiquetas.html, detalle.html                                                                              |
| `truncatewords` | Limita número de palabras                   | articulo_item.html                                                                                                       |
| `date`          | Formatea fecha                             | articulo_item.html, estadisticas_autores.html, estadisticas_secciones.html, detalle.html, articulos_por_fecha.html        |
| `length`        | Obtiene longitud de string/lista           | estadisticas_articulos.html, estadisticas_autores.html                                                                   |
| `floatformat`   | Valor numérico con decimales formateados   | estadisticas_articulos.html, estadisticas_secciones.html                                                                 |
| `intcomma`      | Añade comas como separador de miles         | estadisticas_articulos.html                                                                                              |
| `linebreaks`    | Convierte saltos de línea a `<br>`          | detalle.html                                                                                                             |

---