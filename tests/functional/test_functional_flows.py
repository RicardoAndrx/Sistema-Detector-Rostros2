import pytest
from django.urls import reverse
from django.test import Client
from unittest import mock


@pytest.mark.django_db
class TestFunctionalFlows:
    def setup_method(self):
        self.client = Client()

    def test_asistencia_flow_from_index_to_validate(self):
        """Simula el flujo de llenado de formulario y paso a validación."""
        data = {
            "nombre": "Juan",
            "apellido": "Perez",
            "curso": "3A",
            "materia": "Matemáticas",
        }
        resp = self.client.post(reverse("index"), data)
        assert resp.status_code == 302
        assert resp.url == reverse("validate_view")

        # Ahora accedemos a validate_view con la sesión ya poblada
        resp2 = self.client.get(reverse("validate_view"))
        assert resp2.status_code == 200

    @mock.patch("app.camera.liveness_cam")
    def test_functional_validation_success_and_save(self, mock_cam):
        """Caso funcional: detección exitosa y guardado de asistencia."""
        # Preparamos sesión con datos de formulario
        data = {
            "nombre": "Ana",
            "apellido": "Lopez",
            "curso": "2B",
            "materia": "Física",
        }
        client = Client()
        # Hacemos un POST a index para crear la sesión
        client.post(reverse("index"), data)

        # Simulamos que la cámara ya validó
        mock_cam.status = "¡Validado! Guardando..."
        mock_cam.validation_success = True
        mock_cam.save_assistance.return_value = (True, "Asistencia guardada con éxito.")

        # Frontend preguntaría primero el estado de validación
        status_resp = client.get(reverse("validation_status"))
        assert status_resp.status_code == 200
        assert status_resp.json()["success"] is True

        # Luego llama a process_validation para guardar
        save_resp = client.post(reverse("process_validation"))
        assert save_resp.status_code == 200
        body = save_resp.json()
        assert body["status"] == "ok"
        assert "guardada" in body["message"].lower()

    def test_index_renders_main_interface(self):
        """Verifica que la interfaz principal se carga correctamente."""
        client = Client()
        resp = client.get(reverse("index"))
        assert resp.status_code == 200
        # Busca textos claves del HTML (ajusta si tu plantilla cambia)
        content = resp.content.decode("utf-8").lower()
        assert "registro" in content or "asistencia" in content
        assert "nombre" in content
        assert "apellido" in content
