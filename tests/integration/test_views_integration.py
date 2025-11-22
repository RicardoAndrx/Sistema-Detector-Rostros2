from django.test import TestCase, Client
from django.urls import reverse
from unittest import mock

# Nota: Usa nombres reales de las rutas definidas en app/urls.py
# index, validate_view, video_feed, validation_status, process_validation


class ViewsIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_get(self):
        resp = self.client.get(reverse("index"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Registro de Asistencia", resp.content)

    def test_form_post_redirects_to_validate(self):
        data = {
            "nombre": "Test",
            "apellido": "User",
            "curso": "CursoX",
            "materia": "MateriaY",
        }
        resp = self.client.post(reverse("index"), data)
        # Redirige a validate_view
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers.get("Location"), reverse("validate_view"))

    def test_validate_requires_session(self):
        # Sin datos en sesión debe redirigir a index
        resp = self.client.get(reverse("validate_view"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers.get("Location"), reverse("index"))

    @mock.patch("app.camera.liveness_cam")
    def test_validation_status_success_flow(self, mock_cam):
        # Simular estado exitoso
        mock_cam.status = "¡Validado! Guardando..."
        mock_cam.validation_success = True
        resp = self.client.get(reverse("validation_status"))
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(
            resp.content.decode(),
            {"status": "¡Validado! Guardando...", "success": True},
        )

    @mock.patch("app.camera.liveness_cam")
    def test_process_validation_without_session(self, mock_cam):
        # POST sin form_data en sesión
        mock_cam.save_assistance.return_value = (False, "No se capturó ninguna imagen.")
        resp = self.client.post(reverse("process_validation"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Sesión expirada", resp.content.decode())
