# app/views.py

from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
from django.core.paginator import Paginator
from .models import Asistencia
from django.db import models
from .forms import AsistenciaForm
import csv
from io import BytesIO

from openpyxl import Workbook

# --- Importamos la nueva instancia de la cámara ---
from .camera import liveness_cam
import time


def index(request):
    """Pantalla principal: formulario + historial con filtros y paginación."""
    if request.method == "POST":
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            request.session["form_data"] = form.cleaned_data
            return redirect("validate_view")
    else:
        form = AsistenciaForm()

    # --- Filtros por GET ---
    curso_q = request.GET.get("curso", "").strip()
    materia_q = request.GET.get("materia", "").strip()
    search_q = request.GET.get("q", "").strip()

    asistencias_qs = Asistencia.objects.all().order_by("-fecha_registro")

    if curso_q:
        asistencias_qs = asistencias_qs.filter(curso__icontains=curso_q)
    if materia_q:
        asistencias_qs = asistencias_qs.filter(materia__icontains=materia_q)
    if search_q:
        # Busca en nombre y apellido
        asistencias_qs = asistencias_qs.filter(
            (
                models.Q(nombre__icontains=search_q)
                | models.Q(apellido__icontains=search_q)
            )
        )

    # --- Paginación ---
    page_number = request.GET.get("page", 1)
    paginator = Paginator(asistencias_qs, 5)  # 5 registros por página
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "asistencias": page_obj,
        "curso_q": curso_q,
        "materia_q": materia_q,
        "search_q": search_q,
        "page_obj": page_obj,
    }
    return render(request, "index.html", context)


def export_asistencias_excel(request):
    """Exporta las asistencias filtradas actualmente a un archivo Excel."""
    curso_q = request.GET.get("curso", "").strip()
    materia_q = request.GET.get("materia", "").strip()
    search_q = request.GET.get("q", "").strip()

    qs = Asistencia.objects.all().order_by("-fecha_registro")
    if curso_q:
        qs = qs.filter(curso__icontains=curso_q)
    if materia_q:
        qs = qs.filter(materia__icontains=materia_q)
    if search_q:
        qs = qs.filter(
            (
                models.Q(nombre__icontains=search_q)
                | models.Q(apellido__icontains=search_q)
            )
        )

    wb = Workbook()
    ws = wb.active
    ws.title = "Asistencias"

    ws.append(["ID", "Nombre", "Apellido", "Curso", "Materia", "Fecha registro"])
    for a in qs:
        ws.append(
            [
                a.id,
                a.nombre,
                a.apellido,
                a.curso,
                a.materia,
                a.fecha_registro.strftime("%d/%m/%Y %H:%M"),
            ]
        )

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="asistencias.xlsx"'
    return response


def export_asistencias_pdf(request):
    """Exporta las asistencias filtradas a un PDF sencillo usando FPDF."""
    from fpdf import FPDF

    curso_q = request.GET.get("curso", "").strip()
    materia_q = request.GET.get("materia", "").strip()
    search_q = request.GET.get("q", "").strip()

    qs = Asistencia.objects.all().order_by("-fecha_registro")
    if curso_q:
        qs = qs.filter(curso__icontains=curso_q)
    if materia_q:
        qs = qs.filter(materia__icontains=materia_q)
    if search_q:
        qs = qs.filter(
            (
                models.Q(nombre__icontains=search_q)
                | models.Q(apellido__icontains=search_q)
            )
        )

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Listado de asistencias", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", "", 10)
    for a in qs:
        linea = f"{a.id} - {a.nombre} {a.apellido} | {a.curso} | {a.materia} | {a.fecha_registro.strftime('%d/%m/%Y %H:%M')}"
        pdf.multi_cell(0, 6, linea)

    pdf_output = pdf.output(dest="S").encode("latin-1", "ignore")

    response = HttpResponse(pdf_output, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="asistencias.pdf"'
    return response


# Vista validate_view (sin cambios)
def validate_view(request):
    form_data = request.session.get("form_data")
    if not form_data:
        return redirect("index")

    # Reseteamos el estado de la cámara cada vez que se carga la página
    liveness_cam.__init__()  # Reinicia la cámara y los contadores

    return render(request, "validate.html")


# --- FUNCIÓN GENERADORA MODIFICADA ---
def gen(camera):
    while True:
        frame_bytes, status, success = camera.get_frame()

        if frame_bytes:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n\r\n"
            )

        # Enviamos el estado como una cabecera HTTP
        # (El JS no puede leer esto, usaremos el endpoint de status)
        # Lo dejamos por si acaso, pero crearemos un endpoint mejor

        if success:
            print("Validación exitosa, deteniendo stream.")
            break  # Detiene el generador si la validación fue exitosa

        time.sleep(0.05)  # Pequeña pausa para no sobrecargar el CPU


# --- VISTA VIDEO_FEED MODIFICADA ---
def video_feed(request):
    # Usamos la instancia global 'liveness_cam'
    return StreamingHttpResponse(
        gen(liveness_cam), content_type="multipart/x-mixed-replace; boundary=frame"
    )


# --- VISTA NUEVA: Para que el JS pregunte el estado ---
def validation_status(request):
    """
    Provee al frontend el estado actual de la validación.
    """
    return JsonResponse(
        {"status": liveness_cam.status, "success": liveness_cam.validation_success}
    )


# --- VISTA NUEVA: Para guardar la asistencia ---
def process_validation(request):
    """
    Se llama desde JS cuando 'validation_status' devuelve success=True.
    Guarda la asistencia en la BD.
    """
    if request.method == "POST":
        form_data = request.session.get("form_data")
        if not form_data:
            return JsonResponse({"status": "error", "message": "Sesión expirada."})

        # Usamos la instancia de la cámara para guardar la foto
        success, message = liveness_cam.save_assistance(form_data)

        if success:
            # Limpiamos la sesión después de guardar
            request.session.pop("form_data", None)
            return JsonResponse({"status": "ok", "message": message})
        else:
            return JsonResponse({"status": "error", "message": message})

    return JsonResponse({"status": "error", "message": "Método no permitido"})
