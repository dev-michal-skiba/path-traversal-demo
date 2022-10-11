from io import BytesIO

from django.http import FileResponse
from reportlab.pdfgen import canvas

from account.decorators import protected_view


@protected_view
def download_file_safe(request, context):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, "Hello world.")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, filename='hello.pdf')


@protected_view
def download_file_unsafe(request, context):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, "Hello HELL!")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, filename='hello.pdf')
