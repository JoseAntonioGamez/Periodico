# Periódico - Documentación

Se ha procedido a la creación de objetos en la base de datos mediante Seeder y Faker, además de crear un backup de los datos con fixture.

## Breve descripción de cada función en generar_datos

### generate_autores(self)

Crea 10 registros de autores con datos simulados como nombres, biografías, edades, sueldos y campos booleanos.

---

### generate_usuarios(self)

Crea 10 usuarios con nombres únicos, estado premium y puntos aleatorios.

---

### generate_secciones(self)

Crea 10 secciones temáticas del periódico, asignando nombre, descripción, importancia y estado activo.

---

### generate_etiquetas(self)

Crea 10 etiquetas con nombre, color y descripción para clasificar artículos.

---

### generate_eventos(self)

Crea 10 eventos con nombres creativos, ubicaciones, fechas y capacidad estimada.

---

### generate_grupos(self)

Crea 10 grupos para organizar usuarios, con nombres y descripciones variadas.

---

### generate_articulos(self)

Crea 10 artículos vinculados a autores y secciones aleatorias, con títulos únicos, contenido y visitas simuladas.

---

### generate_portadas(self)

Crea hasta 10 portadas vinculadas a artículos diferentes, respetando la restricción del artículo principal.

---

### generate_perfiles(self)

Crea nuevos perfiles para autores y usuarios, asignando datos de contacto y preferencias aleatorias.

---

### generate_articulo_etiquetas(self)

Crea 10 relaciones entre artículos y etiquetas con atributos adicionales como relevancia, fecha y comentarios.

---

### generate_comentarios(self)

Crea comentarios simulados de usuarios en artículos, con texto y puntuación aleatoria.
