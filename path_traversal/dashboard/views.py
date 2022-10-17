from django.shortcuts import render

from account.decorators import protected_view
from storage.forms import FileForm
from storage.models import SFTPFile


@protected_view
def dashboard(request, context):
    if request.method == 'POST':
        file_form = FileForm(request.POST)
        if file_form.is_valid():
            file_form.save(user=request.user)

    file_form = FileForm()
    filenames = [
        file.filename
        for file
        in SFTPFile.objects.filter(user=request.user).order_by(
            '-year', '-month'
        )
    ]
    context.update({'form': file_form, 'filenames': filenames})
    return render(request, 'dashboard.html', context)
