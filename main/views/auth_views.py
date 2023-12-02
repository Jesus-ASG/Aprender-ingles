from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView

from main.forms import NewUserForm


class Login(FormView):
    template_name = 'no-logged/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, *kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        if token:
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'Nombre de usuario o contraseña incorrectos.')
        return super(Login, self).form_invalid(form)


class Logout(APIView):
    def get(self, request, format=None):
        # if a token auth exists, leave session and delete token
        try:
            if request.user.auth_token is not None:
                request.user.auth_token.delete()
                logout(request)
                return HttpResponseRedirect(reverse_lazy('index'))
        except AttributeError:
            # if there aren't a token send 404 not found
            return HttpResponseNotFound('')


def register(request):
    if request.method == 'GET':
        form = NewUserForm()
        return render(request, 'no-logged/register.html', {'register_form': form})

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            print('Form for register is valid')
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user_auth = authenticate(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=user_auth)
            if token:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('index'))

        else:
            errors = {}

            if 'username' in form.errors:
                # Username already exists
                errors['username'] = 'El nombre de usuario ya está registrado. Por favor, elige otro.'
            if 'password2' in form.errors:
                # Password does not meet requirements
                errors['password'] = form.errors['password2']


        #form = NewUserForm()
        return render(request, 'no-logged/register.html', {'register_form': form, 'errors': errors})

    