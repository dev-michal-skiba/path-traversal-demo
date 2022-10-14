from io import BytesIO

from django.http import FileResponse, Http404
from reportlab.pdfgen import canvas

from account.decorators import protected_view

from storage.utils import get_pdf_from_request


@protected_view
def download_file_safe(request, context):
    filename, pdf_bytes = get_pdf_from_request(request=request)
    if not pdf_bytes:
        raise Http404
    buffer = BytesIO(pdf_bytes)
    p = canvas.Canvas(buffer)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, filename=filename)


@protected_view
def download_file_unsafe(request, context):
    filename, pdf_bytes = get_pdf_from_request(request=request, safe=False)
    if not pdf_bytes:
        raise Http404
    buffer = BytesIO(pdf_bytes)
    p = canvas.Canvas(buffer)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, filename=filename)
