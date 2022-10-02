from http.client import HTTPResponse
from django.shortcuts import render, redirect

from rest_framework import generics
from .models import User
from .serializers import UserSerializer

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .forms import NewUserForm
from django.contrib import messages

from .models import Categorias
from .forms import CategoriasForm


class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)


class Login(FormView):
    template_name = 'urls/login.html'
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


class Index(APIView):
    def get(self, request, format=None):
        try:
            # if a token exists return data
            if request.user.auth_token is not None:
                # if request.user.is_superuser:
                #     return render(request, 'urls/home_admin.html')
                return render(request, 'urls/home.html')
        except AttributeError:
            # if a token doesn't exists return mainpage
            return render(request, 'urls/index.html')


class IndexAdmin(APIView):
    def get(self, request, format=None):
        try:
            # if a token exists return data
            if request.user.auth_token is not None:
                if request.user.is_superuser:
                    return render(request, 'admin/home_admin.html')
                return render(request, 'urls/home.html')
        except AttributeError:
            # if a token doesn't exists return mainpage
            return render(request, 'urls/index.html')

def agregarHistorias(request):
    return render(request, 'admin/historias/agregar_historias.html')


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user_auth = authenticate(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=user_auth)
            if token:
                login(request, user)

            #auth = authenticate(form.cleaned_data['username'], form.cleaned_data['password'])
            #token, _ = Token.objects.get_or_create(user=auth)
            #if token:
            #    login(request, user)

            # return redirect("index")
            # 1 = state
            #render(request, 'urls/register.html', {'state': '1'})
                return HttpResponseRedirect(reverse_lazy('index'))

    form = NewUserForm()
    return render(request, 'urls/register.html', {'register_form': form})


# Categorías

def verCategorias(request):
    categorias = Categorias.objects.all()
    return render(request, 'admin/categorias/ver_categorias.html', {'categorias': categorias})

def agregarCategorias(request):
    formulario = CategoriasForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
    return render(request, 'admin/categorias/agregar_categorias.html', {'formulario': formulario})

def editarCategoria(request, id):
    categoria = Categorias.objects.get(id=id)
    formulario = CategoriasForm(request.POST or None, instance=categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
    return render(request, 'admin/categorias/editar_categoria.html', {'formulario': formulario})

def eliminarCategoria(request, id):
    categoria = Categorias.objects.get(id=id)
    categoria.delete()
    return redirect('ver_categorias')


