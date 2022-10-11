from django.shortcuts import render

from account.decorators import protected_view


@protected_view
def dashboard(request, context):
    return render(request, 'dashboard.html', context)
