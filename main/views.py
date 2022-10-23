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

from .models import Categoria, Historia
from .forms import CategoriaForm, HistoriaForm, PaginaForm


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
                    historias = Historia.objects.all()
                    #for i in range(len(historias)):
                    #    historias[i].titulo_url = self.clearString(historias[i].titulo)
                    return render(request, 'admin/home_admin.html', {'historias': historias})
                return render(request, 'urls/not_found.html')
        except AttributeError:
            # if a token doesn't exists return mainpage
            return render(request, 'urls/index.html')

    @staticmethod
    def clearString(string):
        temp = string.lower().replace(' ', '-').replace('\\', '')
        temp = temp.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        print(f'\n\n\n{temp}')
        return temp

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

# ADMIN #

# Categorías

def verCategorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'admin/categorias/ver_categorias.html', {'categorias': categorias})

def agregarCategorias(request):
    formulario = CategoriaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
    return render(request, 'admin/categorias/agregar_categorias.html', {'formulario': formulario})

def editarCategoria(request, id):
    categoria = Categoria.objects.get(id=id)
    formulario = CategoriaForm(request.POST or None, instance=categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
    return render(request, 'admin/categorias/editar_categoria.html', {'formulario': formulario})

def eliminarCategoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('ver_categorias')


# Historias

def verHistorias(request):
    historias = Historia.objects.all()
    return render(request, 'admin/historias/ver_historias.html', {'historias': historias})

def agregarHistorias(request):
    # form request
    historiaFR = HistoriaForm(request.POST or None, request.FILES or None)
    paginaFR = PaginaForm(request.POST or None)
    
    if historiaFR.is_valid():
        # form object
        historiaFO = historiaFR.save()
        # Crear form object de la página
        if paginaFR.is_valid():
            num_paginas = int(request.POST.get('num_paginas'))
            for i in range(num_paginas):
                
                texto = request.POST.get('texto_'+str(i))
                paginaFO = paginaFR.save(commit=False)
                paginaFO.texto = texto
                paginaFO.historia = historiaFO
                paginaFO.save()
                paginaFR = PaginaForm()
        
        return redirect('ver_historias')
    return render(request, 'admin/historias/agregar_historias.html', 
    {'formulario': historiaFR, 'form_pagina': paginaFR})

def editarHistoria(request, id):
    historia = Historia.objects.get(id=id)
    # obtiene la portada original
    port1 = historia.get_portada()
    formulario = HistoriaForm(request.POST or None, request.FILES or None, instance=historia)
    if formulario.is_valid() and request.POST:
        # obtiene la portada del formulario
        port2 = historia.get_portada()
        # si las portadas son diferentes, entonces borra la anterior
        if port1 != port2:
            historia.del_portada(port1)
        # guarda los datos
        formulario.save()
        return redirect('ver_historias')
    return render(request, 'admin/historias/editar_historia.html', {'formulario': formulario})

def eliminarHistoria(request, id):
    historia = Historia.objects.get(id=id)
    historia.delete()
    return redirect('ver_historias')


# Renderizar historia

def renderizarHistoria(request, titulo):
    return render(request, 'admin/historias/editar_historia.html')