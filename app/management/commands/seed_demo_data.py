import random
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from app.models import Asistencia


class Command(BaseCommand):
    help = "Crea datos de ejemplo para el sistema de registro facial"

    def handle(self, *args, **options):
        nombres = ["Fiorella", "Ricardo", "Ana", "Carlos", "Lucía", "Mateo"]
        apellidos = ["Cabeza", "Salazar", "Lopez", "García", "Pérez", "Ramírez"]
        cursos = ["1ro A", "2do B", "3ro C", "5to nivel B1"]
        materias = ["Construcción de Software", "Matemáticas", "Física", "Programación"]

        try:
            from PIL import Image, ImageDraw
        except ImportError:
            self.stdout.write(
                self.style.WARNING(
                    "Pillow no está instalado; se crearán asistencias sin imagen."
                )
            )
            Image = None

        created = 0
        for i in range(10):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            curso = random.choice(cursos)
            materia = random.choice(materias)

            asistencia = Asistencia(
                nombre=nombre,
                apellido=apellido,
                curso=curso,
                materia=materia,
                fecha_registro=timezone.now(),
            )

            if Image is not None:
                # Crear una imagen simple con fondo y texto "Demo"
                img = Image.new("RGB", (200, 200), color=(30, 64, 175))  # azul oscuro
                draw = ImageDraw.Draw(img)
                draw.text((60, 90), "Demo", fill=(255, 255, 255))

                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                image_content = ContentFile(buffer.getvalue())

                filename = f"demo_{i+1}.jpg"
                asistencia.imagen_asistencia.save(filename, image_content, save=False)

            asistencia.save()
            created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Se crearon {created} asistencias de ejemplo.")
        )
