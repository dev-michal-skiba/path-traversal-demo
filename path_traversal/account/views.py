from django.contrib.auth import (
    authenticate, login as auth_login, logout as auth_logout
)
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from path_traversal import settings

from account.decorators import only_anonymous_view, protected_view
from account.forms import LoginForm, RegisterForm


@only_anonymous_view
def home(request, context):
    return render(request, 'home.html', context)


@only_anonymous_view
def login(request, context):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(settings.DASHBOARD_URL)
    login_form = LoginForm()
    context.update({'form': login_form, 'btn_text': 'Log In'})
    return render(request, 'account_form.html', context)


@protected_view
def logout(request, context):
    auth_logout(request)
    return redirect(settings.HOME_URL)


@only_anonymous_view
def register(request, context):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            if user is not None:
                auth_login(request, user)
                return redirect(settings.DASHBOARD_URL)
    register_form = RegisterForm()
    context.update({'form': register_form, 'btn_text': 'Register'})
    return render(request, 'account_form.html', context)
