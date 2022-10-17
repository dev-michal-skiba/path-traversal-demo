from django.http import FileResponse, Http404

from account.decorators import protected_view

from storage.utils import get_pdf_from_request


@protected_view
def download_file_safe(request, context):
    filename, pdf = get_pdf_from_request(request=request)
    if not pdf:
        raise Http404
    return FileResponse(pdf, filename=filename)


@protected_view
def download_file_unsafe(request, context):
    filename, pdf = get_pdf_from_request(request=request, safe=False)
    if not pdf:
        raise Http404
    return FileResponse(pdf, filename=filename)
