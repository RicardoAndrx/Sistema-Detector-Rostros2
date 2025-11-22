from django.db import models
from django.utils import timezone


# Define la función para la ruta de guardado de la imagen
def ruta_guardado_asistencia(instance, filename):
    # El archivo se guardará en: media/asistencias/CURSO/NOMBRE_APELLIDO_FECHA.jpg
    fecha = timezone.now().strftime('%Y-%m-%d')
    return f'asistencias/{instance.curso}/{instance.nombre}_{instance.apellido}_{fecha}.jpg'


class Asistencia(models.Model):
    # Campos del formulario
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    materia = models.CharField(max_length=100)

    # Campo para la foto
    # 'upload_to' usa la función que definimos arriba para generar una ruta única
    imagen_asistencia = models.ImageField(upload_to=ruta_guardado_asistencia)

    # Campo de fecha y hora, se añade automáticamente
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Esto es lo que veremos en el panel de administrador de Django
        return f"{self.nombre} {self.apellido} - {self.curso} ({self.fecha_registro.strftime('%Y-%m-%d')})"