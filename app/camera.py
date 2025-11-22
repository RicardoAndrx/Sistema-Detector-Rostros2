import cv2
import os
import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from .models import Asistencia  # Importamos el modelo


class LivenessCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.eyes_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

        # --- Variables de estado para la prueba de vida ---
        self.status = "Buscando rostro..."  # Mensaje para el usuario
        self.face_detected = False
        self.blink_detected = False
        self.blink_counter = 0
        self.eyes_detected_previously = False

        # --- Variables para el frame ---
        self.last_frame = None  # Guardará el último frame capturado
        self.validation_success = False
        self.camera_available = self.video.isOpened()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        if not self.camera_available:
            self.status = "Cámara no disponible. Verifique conexión y permisos."
            return None, self.status, False

        success, image = self.video.read()
        if not success or image is None:
            self.status = "Error al leer desde la cámara."
            return None, self.status, False

        # Guardamos una copia limpia para la captura final
        clean_frame = image.copy()

        # 1. Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Detectar rostros
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        self.face_detected = len(faces) > 0

        if self.face_detected:
            self.status = "Rostro detectado. Ahora parpadee."

            # Iteramos sobre el primer rostro encontrado
            (x, y, w, h) = faces[0]
            cv2.rectangle(
                image, (x, y), (x + w, y + h), (255, 0, 0), 2
            )  # Rectángulo azul en rostro

            # Definimos las "Regiones de Interés" (ROI) para los ojos
            roi_gray = gray[y : y + h, x : x + w]
            roi_color = image[y : y + h, x : x + w]

            # 3. Detectar ojos DENTRO del rostro
            eyes = self.eyes_cascade.detectMultiScale(roi_gray, 1.1, 4)

            # Dibujamos rectángulos en los ojos
            for ex, ey, ew, eh in eyes:
                cv2.rectangle(
                    roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
                )  # Verde

            # --- LÓGICA DE PARPADEO ---
            if self.eyes_detected_previously and len(eyes) == 0:
                # Si antes veíamos ojos y AHORA NO (y seguimos viendo la cara), es un parpadeo
                self.blink_counter += 1
                self.status = f"Parpadeo detectado! {self.blink_counter}/1"

            self.eyes_detected_previously = len(eyes) > 0

            # 4. Validación Exitosa
            if self.blink_counter >= 1:  # Pedimos 1 parpadeo
                self.status = "¡Validado! Guardando..."
                self.validation_success = True
                self.last_frame = clean_frame  # Guardamos la imagen limpia
                cv2.putText(
                    image,
                    "VALIDADO",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

        else:
            self.status = "Buscando rostro..."
            self.eyes_detected_previously = False  # Reseteamos si se pierde el rostro
            self.blink_counter = 0

        # Codificar la imagen anotada para el stream
        ret, jpeg = cv2.imencode(".jpg", image)

        # Devolvemos el frame y el estado actual
        return jpeg.tobytes(), self.status, self.validation_success

    def save_assistance(self, form_data):
        if self.last_frame is None:
            return False, "No se capturó ninguna imagen."

        try:
            # 1. Crear una nueva instancia del modelo Asistencia
            asistencia = Asistencia(
                nombre=form_data["nombre"],
                apellido=form_data["apellido"],
                curso=form_data["curso"],
                materia=form_data["materia"],
            )

            # 2. Convertir el frame de OpenCV (array numpy) a un archivo de imagen
            ret, buf = cv2.imencode(".jpg", self.last_frame)
            image_content = ContentFile(buf.tobytes())

            # 3. Generar un nombre de archivo
            now = datetime.datetime.now()
            filename = (
                f"asistencia_{form_data['nombre']}_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
            )

            # 4. Asignar la imagen al campo ImageField y guardar
            asistencia.imagen_asistencia.save(filename, image_content, save=True)

            # 5. Guardar la instancia completa en la BD
            asistencia.save()

            return True, "Asistencia guardada con éxito."

        except Exception as e:
            print(f"Error al guardar: {e}")
            return False, f"Error interno del servidor: {e}"


# --- Instancia global (Singleton) ---
# Creamos una única instancia de la cámara para que sea compartida
# entre la vista del 'video_feed' y la vista de 'guardar'
liveness_cam = LivenessCamera()
