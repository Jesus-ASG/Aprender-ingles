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
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .forms import NewUserForm
from django.contrib import messages

from .models import Categoria, Historia, Page
from .forms import CategoriaForm, HistoriaForm, PaginaForm

# Dar formato
import re


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


def index(request):
    try:
        # if a token exists return data
        user = request.user
        if user.auth_token is not None:
            historias = Historia.objects.all()
            
            return render(request, 'urls/index.html', {'historias':historias, 'user':user})
    except AttributeError:
        # if a token doesn't exists return to homepage
        return render(request, 'urls/home.html')


def myAdmin(request):
    try:
        # if a token exists return data
        if request.user.auth_token is not None:
            if request.user.is_superuser:
                #historias = Historia.objects.all()
                #return render(request, 'urls/index.html', {'historias': historias})
                return redirect('ver_historias')
            return render(request, 'urls/index.html')
    except AttributeError:
        # if a token doesn't exists return mainpage
        return render(request, 'urls/home.html')
    

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
class Response:
    def __init__(self):
        self.alert = ''
        self.message = ''
    
    def setAlert(self, alert):
        match alert:
            case 'danger':
                self.alert = 'alert-danger'
    
    def setMessage(self, message):
        self.message = message
        

def verHistorias(request):
    historias = Historia.objects.all()
    return render(request, 'admin/historias/ver_historias.html', {'historias': historias})

def agregarHistorias(request):
    historiaFR = HistoriaForm(request.POST or None, request.FILES or None)
    paginaFR = PaginaForm(request.POST or None)
    
    if not historiaFR.is_valid():
        return render(request, 'admin/historias/agregar_historias.html', 
        {'formulario': historiaFR, 'form_pagina': paginaFR})
    
    historiaFO = historiaFR.save(commit=False)
    historiaFO.titulo = re.sub(' +', ' ', historiaFO.titulo)
    
    try:
        duplicado = Historia.objects.get(titulo=historiaFO.titulo)
        if duplicado:
            resp = Response()
            resp.setAlert('danger')
            resp.setMessage('Ya existe una historia con ese título')
            return render(request, 'admin/historias/agregar_historias.html', 
            {'formulario': historiaFR, 'form_pagina': paginaFR, 'resp': resp})
    except:
        #does nothing because save() method already save slug
        pass

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
    
def editarHistoria(request, id):
    historia = Historia.objects.get(id=id)
    # obtiene portada y ruta del objeto
    port1 = historia.get_portada()
    first_title = re.sub(' +', ' ', historia.titulo)

    fR = HistoriaForm(request.POST or None, request.FILES or None, instance=historia)
    if fR.is_valid() and request.POST:
        #### Cambiar ruta si es que modificó el título, ya que la ruta se basa en el título ####
        historia.titulo = re.sub(' +', ' ', historia.titulo)
        if first_title != historia.titulo:
            try:
                duplicado = Historia.objects.get(titulo=historia.titulo)
                if duplicado:
                    resp = Response()
                    resp.setAlert('danger')
                    resp.setMessage('Ya existe una historia con ese título')
                    return render(request, 'admin/historias/agregar_historias.html', 
                    {'formulario': fR, 'form_pagina': fR, 'resp': resp})
            except:
                #does nothing because save() method already save slug
                pass
        #### Portada ####
        # obtiene la portada del formulario
        port2 = historia.get_portada()
        # si las portadas son diferentes, entonces borra la anterior
        if port1 != port2:
            historia.del_portada(port1)
        fR.save()
        return redirect('ver_historias')
    return render(request, 'admin/historias/editar_historia.html', {'formulario': fR})

def eliminarHistoria(request, id):
    historia = Historia.objects.get(id=id)
    historia.delete()
    return redirect('ver_historias')

# Renderizar información de la historia
def infoHistoria(request, ruta):
    try:
        historia = Historia.objects.get(ruta=ruta)
        paginas = Page.objects.filter(historia = historia.id)
        has_pages = False
        if len(paginas) > 0:
            has_pages = True
        args = {'historia': historia, 'has_pages':has_pages}
    except:
        return HttpResponseNotFound()
    return render(request, 'urls/info_historia.html', args)

def contenidoHistoria(request, ruta, num_pagina):
    try:
        historia = Historia.objects.get(ruta=ruta)
        paginas = Page.objects.filter(historia = historia.id)
        continua = True
        if num_pagina>=len(paginas):
            continua = False
        pagina = paginas[num_pagina-1]
        prueba = '<a href="https://www.google.com">Elemento a</a><div class="rojo">Elemento div</div>'
        args = {'historia': historia, 'pagina': pagina, 'continua':continua,
        'ruta': ruta, 'num_pagina':num_pagina+1, 'prueba':prueba}
    except:
        return HttpResponseNotFound()
    
    

    return render(request, 'urls/contenido_historia.html', args)