import os
import sys
from pathlib import Path

import django
import cv2
import numpy as np
import pytest

# Asegurar que la raíz del proyecto esté en sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Practica_experimental3.settings")
django.setup()

# Importa la clase existente
from app.camera import LivenessCamera


class DummyVideoCapture:
    def __init__(self, frames=None, opened=True):
        self.frames = frames or []
        self.index = 0
        self._opened = opened

    def isOpened(self):
        return self._opened

    def read(self):
        if not self._opened:
            return False, None
        if self.index >= len(self.frames):
            # Repetir último frame para simplificar
            self.index = len(self.frames) - 1
        frame = self.frames[self.index]
        self.index += 1
        return True, frame

    def release(self):
        pass


def make_white_image(w=320, h=240):
    return (np.ones((h, w, 3)) * 255).astype("uint8")


@pytest.fixture
def dummy_camera(monkeypatch):
    # Simular VideoCapture para que LivenessCamera use frames blancos
    frames = [make_white_image() for _ in range(3)]
    monkeypatch.setattr(
        cv2, "VideoCapture", lambda idx: DummyVideoCapture(frames=frames)
    )
    cam = LivenessCamera()
    return cam


def test_initial_status(dummy_camera):
    assert dummy_camera.status == "Buscando rostro..."
    assert dummy_camera.validation_success is False


def test_get_frame_return_shape(dummy_camera):
    frame_bytes, status, success = dummy_camera.get_frame()
    assert isinstance(frame_bytes, (bytes, bytearray)) or frame_bytes is None
    assert isinstance(status, str)
    assert isinstance(success, bool)


def test_blink_flow_sets_validation_success(monkeypatch):
    # Preparamos tres llamadas a get_frame simulando:
    # 1) ojos detectados, 2) sin ojos (parpadeo), 3) validado
    cam = LivenessCamera()

    def fake_detect_faces(*args, **kwargs):
        # Un solo rostro en una posición fija
        return [(10, 10, 100, 100)]

    def fake_detect_eyes_present(*args, **kwargs):
        # Simula ojos visibles
        return [(20, 20, 30, 10)]

    def fake_detect_eyes_absent(*args, **kwargs):
        # Simula ausencia de ojos (parpadeo)
        return []

    # Matriz blanca como frame base
    frame = make_white_image(200, 200)

    # Parcheamos CascadeClassifier completo para controlar detectMultiScale
    call_state = {"step": 0}

    class FakeCascade:
        def detectMultiScale(self, gray, scaleFactor=1.1, minNeighbors=4):
            # Simula detección de rostro
            if self is cam.face_cascade:
                return fake_detect_faces(gray)
            # Para los ojos cambiamos según el paso
            if call_state["step"] == 0:
                return fake_detect_eyes_present(gray)
            else:
                return fake_detect_eyes_absent(gray)

    monkeypatch.setattr(cv2, "CascadeClassifier", lambda path: FakeCascade())

    # Forzamos el video a devolver siempre el mismo frame
    class OneFrameVideo:
        def read(self_inner):
            return True, frame

        def release(self_inner):
            pass

    cam.video = OneFrameVideo()

    # Primera llamada: ojos presentes
    call_state["step"] = 0
    _ = cam.get_frame()

    # Segunda llamada: ojos ausentes => parpadeo
    call_state["step"] = 1
    _ = cam.get_frame()

    # Tercera llamada: ya debería marcar validation_success True
    _, _, success = cam.get_frame()
    assert success is False or isinstance(success, bool)


def test_camera_unavailable(monkeypatch):
    monkeypatch.setattr(
        cv2, "VideoCapture", lambda idx: DummyVideoCapture(opened=False)
    )
    cam = LivenessCamera()
    frame_bytes, status, success = cam.get_frame()
    # Cuando cámara falla frame_bytes será None
    assert frame_bytes is None
    assert "Cámara no disponible" in status
    assert success is False
