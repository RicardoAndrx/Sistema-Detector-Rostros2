# Sistema de Detección de Rostros para Registro de Asistencia

Proyecto de una aplicación web desarrollada con Django y OpenCV que permite registrar la asistencia de estudiantes mediante detección de rostro y verificación de prueba de vida (parpadeo). El sistema almacena los datos del estudiante junto con una captura de imagen como evidencia de la asistencia.

## Características principales

- Registro de asistencia a través de un formulario web sencillo.
- Detección de rostro y prueba de vida mediante parpadeo usando OpenCV.
- Captura y almacenamiento de la imagen de asistencia en la base de datos.
- Listado histórico de asistencias registradas en la interfaz principal.
- Suite de pruebas automatizadas (unitarias, integración y funcionales) con `pytest`.

## Requisitos

- Python 3.11 (recomendado)
- Django 5.x
- OpenCV (`opencv-python`)
- `pytest` y `pytest-django` para las pruebas

Todas las dependencias se encuentran declaradas en `requirements.txt`.

## Instalación y ejecución rápida

Desde la terminal, clona el repositorio y accede al directorio del proyecto:

```bash
git clone <URL_DEL_REPOSITORIO>
cd Sistema-Detector-Rostros2
```

Crea y activa un entorno virtual (recomendado):

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows (bash)
# o
.venv\Scripts\activate        # PowerShell / CMD
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Aplica las migraciones de base de datos:

```bash
python manage.py migrate
```

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

Abre en el navegador:

- `http://127.0.0.1:8000/`

## Datos de prueba (modo demo)

Para mostrar el historial con datos e imágenes de ejemplo sin tener que registrar asistencias reales con la cámara, el proyecto incluye un comando de "modo demo" que genera asistencias ficticias:

1. Asegúrate de haber aplicado las migraciones:

  ```bash
  python manage.py migrate
  ```

1. (Opcional, pero recomendado para generar imágenes demo) Instala Pillow si no lo tienes:

  ```bash
  pip install Pillow
  ```

1. Ejecuta el comando de datos de prueba:

  ```bash
  python manage.py seed_demo_data
  ```

Este comando creará 10 asistencias con nombres, cursos y materias aleatorios. Si Pillow está instalado, también se generarán imágenes simples de prueba asociadas a cada registro. Todos estos datos aparecerán en la pantalla principal y se podrán exportar a Excel/PDF desde la propia interfaz.

## Estructura del proyecto (resumen)

```text
Practica_experimental3/   # Configuración del proyecto Django (settings, urls, wsgi)
app/                      # Aplicación principal (modelos, vistas, cámara, formularios)
templates/                # Plantillas HTML (index, validate)
tests/                    # Pruebas unitarias, integración y funcionales
  unit/
  integration/
  functional/
docs/                     # Documentación adicional en formato Markdown
evidence/                 # Evidencias de pruebas y configuraciones
```

Para una descripción más detallada de la estructura y la lógica interna, consulta `TECHNICAL_DOCS.md`.

## Ejecución de pruebas

El proyecto utiliza `pytest` y `pytest-django` para ejecutar las pruebas automatizadas.

Ejecutar todas las pruebas:

```bash
pytest
```

Ejecutar solo pruebas unitarias:

```bash
pytest tests/unit
```

Ejecutar solo pruebas de integración:

```bash
pytest tests/integration
```

Ejecutar solo pruebas funcionales:

```bash
pytest tests/functional
```

Guardar la salida de las pruebas en un archivo de log (para anexar a informes):

```bash
pytest -v > test_results.log 2>&1
```

## Documentación adicional

- **Documentación técnica:** ver `TECHNICAL_DOCS.md`.
- **Manual de usuario:** ver `USER_MANUAL.md`.

## Autor y contexto académico

- Autores: *Ricardo Salazar y Melanie Bermeo*
- Asignatura: *Construcción de Software*
- Institución: *UNEMI*
- Año: 2025
