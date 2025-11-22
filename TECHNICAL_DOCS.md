# Documentación Técnica del Sistema de Detección de Rostros

## 1. Descripción general

Este proyecto es una aplicación web desarrollada con Django que permite registrar asistencias mediante detección de rostro y verificación de prueba de vida (parpadeo) utilizando OpenCV. El flujo principal inicia en un formulario de registro de datos del estudiante, continúa con la validación de video y finaliza con el almacenamiento de la evidencia en la base de datos.

## 2. Requisitos del sistema

### 2.1 Software

- Python 3.11 (recomendado, ver `evidence/python_version.txt`).
- Django 5.x.
- OpenCV (`opencv-python`).
- pytest y pytest-django para pruebas automatizadas.
- SQLite (incluido por defecto con Django, usado como base de datos).

### 2.2 Librerías principales (según `requirements.txt`)

- `Django`
- `opencv-python`
- `pytest`
- `pytest-django`

> Nota: Ejecutar `pip install -r requirements.txt` para instalar todas las dependencias.

## 3. Instalación y puesta en marcha

### 3.1 Clonado del repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Sistema-Detector-Rostros2
```

### 3.2 Creación y activación del entorno virtual (opcional pero recomendado)

```bash
python -m venv .venv
source .venv/Scripts/activate  # En Windows (bash)
# o
.venv\Scripts\activate        # En PowerShell / CMD
```

### 3.3 Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 3.4 Migraciones de base de datos

```bash
python manage.py migrate
```

### 3.5 Ejecución del servidor de desarrollo

```bash
python manage.py runserver
```

Luego, acceder en el navegador a `http://127.0.0.1:8000/`.

## 3.6 Datos de prueba (modo demo)

Para facilitar las pruebas sin necesidad de registrar siempre asistencias reales con la cámara, el proyecto incluye un comando de gestión que genera registros de ejemplo.

El comando se encuentra en `app/management/commands/seed_demo_data.py` y crea 10 instancias del modelo `Asistencia` con datos aleatorios y, si se dispone de Pillow, imágenes sencillas de prueba.

Pasos recomendados:

1. Aplicar migraciones (si no se ha hecho):

    ```bash
    python manage.py migrate
    ```

1. (Opcional) Instalar Pillow para generar imágenes demo:

    ```bash
    pip install Pillow
    ```

1. Ejecutar el comando de datos de ejemplo:

    ```bash
    python manage.py seed_demo_data
    ```

Este comando:

- Genera nombres, apellidos, cursos y materias a partir de listas predefinidas.
- Asigna una fecha de registro actual (`timezone.now()`).
- Si Pillow está disponible, crea imágenes JPEG simples (fondo de color y texto "Demo") y las guarda en el campo `imagen_asistencia` del modelo.

Los registros generados se muestran en la vista `index` y permiten probar visualmente:

- El listado e historial de asistencias.
- Los filtros por nombre, curso y materia.
- La paginación.
- La exportación de asistencias a Excel y PDF.

## 4. Estructura de directorios

Árbol simplificado del proyecto:

```text
Sistema-Detector-Rostros2/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── Practica_experimental3/           # Proyecto Django (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── app/                              # Aplicación principal
│   ├── models.py                     # Modelo Asistencia
│   ├── views.py                      # Vistas index, validate_view, video_feed, etc.
│   ├── camera.py                     # Lógica de detección y prueba de vida (OpenCV)
│   ├── forms.py                      # Formulario de registro de asistencia
│   └── ...
├── templates/
│   ├── index.html                    # Formulario principal e historial de asistencias
│   └── validate.html                 # Interfaz de validación de video
├── tests/
│   ├── unit/
│   │   └── test_liveness_camera.py   # Pruebas unitarias del módulo de cámara
│   ├── integration/
│   │   └── test_views_integration.py # Pruebas de integración de vistas y rutas
│   └── functional/
│       └── test_functional_flows.py  # Pruebas funcionales de flujo de uso
├── docs/
│   ├── tecnico.md
│   └── usuario.md
└── evidence/                         # Evidencias de ejecución de pruebas y versiones
    └── ...
```

## 5. Explicación de pruebas

El proyecto utiliza `pytest` y `pytest-django` para ejecutar las pruebas automatizadas. Se organizan en tres niveles: **unitarias**, **integración** y **funcionales**.

### 5.1 Pruebas unitarias (`tests/unit/test_liveness_camera.py`)

Objetivo: Validar la lógica interna del módulo de detección y prueba de vida `LivenessCamera` definido en `app/camera.py`.

Casos cubiertos:

- **Estado inicial de la cámara**: Verifica que al crear una instancia de `LivenessCamera` el estado sea "Buscando rostro..." y que `validation_success` sea `False`.
- **Formato del frame devuelto**: Comprueba que `get_frame()` devuelve bytes de imagen (o `None` cuando no hay frame), un mensaje de estado en texto y un booleano de éxito.
- **Manejo de cámara no disponible**: Simula que `cv2.VideoCapture` no se abre correctamente y valida que el sistema no se rompa, devolviendo un estado coherente para el usuario.
- **Flujo de parpadeo (prueba de vida)**: Simula la detección de rostro y la transición entre ojos detectados y no detectados para comprobar que el contador de parpadeos se actualiza y que la validación de prueba de vida se establece correctamente.

Estas pruebas usan `monkeypatch` para simular la cámara física y garantizar que las pruebas sean reproducibles sin hardware.

### 5.2 Pruebas de integración (`tests/integration/test_views_integration.py`)

Objetivo: Validar el comportamiento de las vistas principales de Django y que las rutas respondan correctamente.

Casos cubiertos:

- **`index` (GET)**: Comprueba que la página principal responde con código HTTP 200 y que el contenido HTML contiene textos relacionados con el registro de asistencia.
- **`index` (POST)**: Envío de datos válidos del formulario y verificación de que la vista redirige correctamente a `validate_view`.
- **`validate_view` sin sesión**: Verifica que si se accede a la vista de validación sin datos previos en sesión, el sistema redirige de vuelta a `index` (flujo controlado de navegación).
- **`validation_status`**: Mockea la instancia global `liveness_cam` para simular una validación exitosa y verifica que el endpoint responda con JSON correcto (`status` y `success`).
- **`process_validation` sin sesión**: Envía una petición POST sin datos en sesión y comprueba que el sistema responde con un mensaje de error apropiado.

### 5.3 Pruebas funcionales (`tests/functional/test_functional_flows.py`)

Objetivo: Validar casos de uso completos desde la perspectiva del usuario final y del flujo de negocio.

Casos cubiertos:

- **Flujo de registro de asistencia (formulario → validación)**: Simula el llenado del formulario en `index`, comprueba la redirección a `validate_view` y el acceso correcto a la vista de validación.
- **Flujo completo de validación y guardado**: Mockea `liveness_cam` para indicar una validación exitosa (`success=True`), consulta el endpoint de estado (`validation_status`) y luego llama a `process_validation`, verificando que la respuesta indique que la asistencia fue guardada con éxito.
- **Visualización correcta de la interfaz principal**: Verifica que la vista `index` se renderiza correctamente y que el HTML contiene campos clave como nombre, apellido y referencias a asistencia.

## 6. Cómo ejecutar las pruebas

Desde la raíz del proyecto (`Sistema-Detector-Rostros2/`) y con el entorno virtual activado:

### 6.1 Ejecutar toda la suite de pruebas

```bash
pytest
```

### 6.2 Ejecutar solo un subconjunto de pruebas

- Solo pruebas unitarias:

```bash
pytest tests/unit
```

- Solo pruebas de integración:

```bash
pytest tests/integration
```

- Solo pruebas funcionales:

```bash
pytest tests/functional
```

### 6.3 Guardar la salida de las pruebas en un archivo de log

Para generar un archivo de evidencia (`test_results.log`):

```bash
pytest -v > test_results.log 2>&1
```

Este archivo puede adjuntarse como anexo en el informe o como parte de la carpeta `evidence/`.

## 7. Consideraciones técnicas adicionales

- El sistema utiliza una instancia global `liveness_cam` para compartir la cámara entre la vista de streaming de video y el proceso de guardado de asistencia.
- La lógica de prueba de vida se basa en la detección de rostro y cambios en la detección de ojos (parpadeo), apoyada por clasificadores Haar (`haarcascade_frontalface_default.xml` y `haarcascade_eye.xml`).
- La evidencia de asistencia se almacena en el modelo `Asistencia`, incluyendo una imagen capturada durante la validación.

Con esta estructura y cobertura de pruebas, el proyecto queda preparado para evaluación académica y despliegue básico.
