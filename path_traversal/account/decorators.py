from django.shortcuts import redirect

from path_traversal import settings


def only_anonymous_view(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.DASHBOARD_URL)
        context = {'logged_in': False}
        return func(request, context, *args, **kwargs)
    return inner


def protected_view(func):
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.HOME_URL)
        context = {'logged_in': True}
        return func(request, context, *args, **kwargs)
    return inner
