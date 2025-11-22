from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("validate/", views.validate_view, name="validate_view"),
    path("video_feed/", views.video_feed, name="video_feed"),
    # --- RUTAS NUEVAS ---
    # Para que el JS pregunte el estado (Ej: "Parpadee")
    path("validation_status/", views.validation_status, name="validation_status"),
    # Para que el JS ordene guardar la foto y los datos
    path("process_validation/", views.process_validation, name="process_validation"),
    path(
        "export/excel/", views.export_asistencias_excel, name="export_asistencias_excel"
    ),
    path("export/pdf/", views.export_asistencias_pdf, name="export_asistencias_pdf"),
]
