# Manual de Usuario del Sistema de Detección de Rostros

## 1. Introducción

Este sistema permite registrar la asistencia de estudiantes utilizando detección de rostro y una prueba de vida basada en parpadeo. El usuario final (docente o responsable de asistencia) interactúa a través de una interfaz web sencilla donde ingresa los datos del estudiante y confirma la asistencia mediante la cámara del equipo.

## 2. Requisitos previos para el usuario

- Un ordenador con cámara web funcional.
- Navegador web actualizado (Chrome, Firefox, Edge o similar).
- Acceso a la red local o internet donde se encuentre desplegado el servidor Django.

## 3. Acceso al sistema

1. Abra su navegador web.
2. Ingrese la URL proporcionada por el administrador del sistema, por ejemplo:
   - `http://127.0.0.1:8000/` (en un entorno local de pruebas).

[INSERTAR CAPTURA DE PANTALLA DE LA PÁGINA PRINCIPAL AQUÍ]

## 4. Flujo de uso paso a paso

### 4.1 Registro de datos del estudiante

1. En la página principal, complete el formulario con los siguientes campos:
   - **Nombre** del estudiante.
   - **Apellido** del estudiante.
   - **Curso** (por ejemplo, "3A").
   - **Materia** (por ejemplo, "Matemáticas").

2. Revise que los datos sean correctos.
3. Presione el botón de **Registrar / Continuar** (según la etiqueta del botón en la interfaz).

[INSERTAR CAPTURA DE PANTALLA DEL FORMULARIO DE REGISTRO AQUÍ]

Si los datos son válidos, el sistema lo redirigirá automáticamente a la pantalla de validación de video.

### 4.2 Pantalla de validación de video (prueba de vida)

1. En la página de validación, permita el acceso a la **cámara web** cuando el navegador lo solicite.
2. Coloque el rostro del estudiante frente a la cámara, bien iluminado y centrado.
3. Observe el mensaje en pantalla (estado de validación), que puede indicar, por ejemplo:
   - "Buscando rostro..." (el sistema aún no detecta ningún rostro).
   - "Rostro detectado. Ahora parpadee." (el sistema ha encontrado un rostro y espera un parpadeo).
   - "¡Validado! Guardando..." (la prueba de vida se completó correctamente).

[INSERTAR CAPTURA DE PANTALLA DEL LOGIN / VALIDACIÓN CON CÁMARA AQUÍ]

<!-- 4. Pida al estudiante que **parpadee de forma natural** frente a la cámara. El sistema detectará el parpadeo como señal de que se trata de una persona real y no de una fotografía.

5. Una vez completada la validación, el sistema guardará automáticamente la asistencia y una captura de la imagen en la base de datos. -->

### 4.3 Confirmación y visualización del registro

Después de la validación, el sistema puede:

- Mostrar un mensaje de confirmación en pantalla indicando que la asistencia fue registrada correctamente.
- Redirigir o permitir volver a la página principal donde se listan las últimas asistencias registradas.

En la página principal, generalmente se muestra una tabla con las asistencias más recientes, donde podrá ver:

- Nombre y apellido del estudiante.
- Curso y materia.
- Fecha y hora de registro.
- (Opcionalmente) una miniatura o enlace a la imagen capturada.

[INSERTAR CAPTURA DE PANTALLA DEL LISTADO DE ASISTENCIAS AQUÍ]

## 5. Interpretación de resultados y mensajes

Durante el uso del sistema, pueden aparecer distintos mensajes o estados. A continuación se describen los más importantes y su interpretación:

- **"Buscando rostro..."**:
  - Significa que el sistema aún no encuentra un rostro claramente visible.
  - Recomendaciones:
    - Asegúrese de que la cámara está bien enfocada.
    - Mejore la iluminación del ambiente.
    - Centre el rostro del estudiante en la imagen.

- **"Rostro detectado. Ahora parpadee."**:
  - El sistema ha detectado un rostro y ahora requiere un parpadeo para confirmar que se trata de una persona real.
  - Recomendaciones:
    - Pida al estudiante que parpadee una o dos veces de forma natural.

- **"¡Validado! Guardando..."**:
  - La prueba de vida fue exitosa y el sistema está registrando la asistencia y guardando la imagen.
  - En unos segundos, la asistencia debería aparecer en el listado de la pantalla principal.

- **"No se capturó ninguna imagen." o mensajes de error similares**:
  - Indican que hubo un problema al guardar la asistencia.
  - Recomendaciones:
    - Verificar que la cámara funciona correctamente.
    - Reintentar el proceso desde el formulario inicial.
    - Si el problema persiste, contactar al administrador del sistema.

## 6. Buenas prácticas de uso

- Utilizar el sistema en ambientes bien iluminados para mejorar la detección del rostro.
- Evitar que más de una persona aparezca en la cámara durante la validación.
- Mantener el rostro del estudiante a una distancia adecuada para que la cara ocupe una porción central de la imagen.
- No cubrir los ojos con gafas muy oscuras, mascarillas que tapen demasiado o accesorios que dificulten la detección.

## 7. Preguntas frecuentes (FAQ)

**1. ¿Qué pasa si la cámara no funciona?**

- Compruebe que la cámara esté conectada y reconocida por el sistema operativo.
- Cierre otras aplicaciones que puedan estar usando la cámara (Zoom, Teams, etc.).
- Actualice los controladores de la cámara si es necesario.

**2. ¿Puedo usar el sistema sin cámara?**

- No. La funcionalidad principal del sistema depende de la detección de rostro y la prueba de vida mediante parpadeo, por lo que la cámara es obligatoria.

**3. ¿Se guardan las imágenes de los estudiantes?**

- Sí, el sistema almacena una imagen asociada al registro de asistencia con fines de respaldo y trazabilidad. El tratamiento de estas imágenes debe cumplir las políticas de privacidad y protección de datos de la institución.

## 8. Lugar para anexar capturas en el informe

Use esta sección como guía para insertar capturas de pantalla en el PDF final:

- [INSERTAR CAPTURA DE PANTALLA DEL LOGIN / PANTALLA PRINCIPAL AQUÍ]
- [INSERTAR CAPTURA DE PANTALLA DEL FORMULARIO COMPLETADO AQUÍ]
- [INSERTAR CAPTURA DE PANTALLA DE LA VALIDACIÓN CON CÁMARA Y MENSAJE DE ESTADO AQUÍ]
- [INSERTAR CAPTURA DE PANTALLA DEL LISTADO DE ASISTENCIAS REGISTRADAS AQUÍ]

Con este manual, un usuario final sin conocimientos técnicos avanzados debería ser capaz de utilizar el sistema de forma correcta y entender el significado de los resultados mostrados por la aplicación.
