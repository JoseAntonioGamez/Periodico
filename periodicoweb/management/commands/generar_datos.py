from django.core.management.base import BaseCommand
from faker import Faker
from periodicoweb.models import (
    Autor, PerfilAutor, Usuario, PerfilUsuario,
    Seccion, Articulo, Portada,
    Etiqueta, ArticuloEtiqueta, Evento, Grupo, Comentario
)
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Genera 10 datos aleatorios para cada modelo usando Faker'

    def handle(self, *args, **kwargs):
        self.generate_autores()
        self.generate_usuarios()
        self.generate_secciones()
        self.generate_etiquetas()
        self.generate_eventos()
        self.generate_grupos()
        self.generate_articulos()
        self.generate_portadas()
        self.generate_perfiles()
        self.generate_articulo_etiquetas()
        self.generate_comentarios()
        self.stdout.write(self.style.SUCCESS('Datos de prueba generados correctamente.'))

    def generate_autores(self):
        for _ in range(10):
            Autor.objects.create(
                nombre=fake.unique.name(),
                bio=fake.text(max_nb_chars=200),
                edad=random.randint(18, 80),
                sueldo=round(random.uniform(1000, 5000), 2),
                es_redactor=fake.boolean()
            )

    def generate_usuarios(self):
        for _ in range(10):
            Usuario.objects.create(
                nombre=fake.unique.user_name(),
                es_premium=fake.boolean(),
                puntos=random.randint(0, 500)
            )

    def generate_secciones(self):
        opciones = ['POL', 'DEP', 'CUT']
        for i in range(10):
            Seccion.objects.create(
                nombre=random.choice(opciones),
                descripcion=fake.text(max_nb_chars=100),
                importancia=random.randint(1, 5),
                activa=fake.boolean()
            )

    def generate_etiquetas(self):
        for _ in range(10):
            Etiqueta.objects.create(
                nombre=fake.word(),
                color=fake.hex_color(),
                descripcion=fake.sentence(nb_words=6),
                activa=fake.boolean()
            )

    def generate_eventos(self):
        for _ in range(10):
            Evento.objects.create(
                nombre=fake.catch_phrase(),
                lugar=fake.city(),
                fecha=fake.date_this_year(),
                capacidad=random.randint(10, 500)
            )

    def generate_grupos(self):
        for _ in range(10):
            Grupo.objects.create(
                nombre=fake.word(),
                descripcion=fake.text(max_nb_chars=100)
            )

    def generate_articulos(self):
        autores = list(Autor.objects.all())
        secciones = list(Seccion.objects.all())
        for _ in range(10):
            Articulo.objects.create(
                titulo=fake.unique.sentence(nb_words=6),
                contenido=fake.text(max_nb_chars=1000),
                autor=random.choice(autores),
                seccion=random.choice(secciones),
                visitas=random.randint(0, 1000)
            )

    def generate_portadas(self):
        articulos = list(Articulo.objects.all())
        max_portadas = min(10, len(articulos))
        for i in range(max_portadas):
            articulo = articulos[i]
            if not Portada.objects.filter(articulo_principal=articulo).exists():
                Portada.objects.create(
                    articulo_principal=articulo,
                    mensaje=fake.sentence(nb_words=10),
                    destacado=fake.boolean()
                )

    def generate_perfiles(self):
        autores = list(Autor.objects.all())
        usuarios = list(Usuario.objects.all())

        for autor in autores[:10]:
            if not PerfilAutor.objects.filter(autor=autor).exists():
                PerfilAutor.objects.create(
                    autor=autor,
                    ciudad=fake.city(),
                    telefono=fake.phone_number(),
                    fecha_nacimiento=fake.date_of_birth(),
                    hora_favorita=fake.time()
                )

        for usuario in usuarios[:10]:
            if not PerfilUsuario.objects.filter(usuario=usuario).exists():
                PerfilUsuario.objects.create(
                    usuario=usuario,
                    direccion=fake.address(),
                    telefono=fake.phone_number(),
                    preferencia_hora=fake.time()
                )

    def generate_articulo_etiquetas(self):
        articulos = list(Articulo.objects.all())
        etiquetas = list(Etiqueta.objects.all())
        for _ in range(10):
            ArticuloEtiqueta.objects.create(
                articulo=random.choice(articulos),
                etiqueta=random.choice(etiquetas),
                relevancia=round(random.uniform(0.1, 5.0), 2),
                fecha_asignacion=fake.date_this_year(),
                comentario=fake.sentence(nb_words=8)
            )

    def generate_comentarios(self):
        articulos = list(Articulo.objects.all())
        usuarios = list(Usuario.objects.all())
        for _ in range(10):
            Comentario.objects.create(
                usuario=random.choice(usuarios),
                articulo=random.choice(articulos),
                texto=fake.text(max_nb_chars=300),
                puntuacion=round(random.uniform(0, 5), 1)
            )
    