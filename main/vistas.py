
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
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .forms import NewUserForm

from .models import Story, Page


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
            historias = Story.objects.all()

            return render(request, 'urls/index.html', {'historias': historias, 'user': user})
    except AttributeError:
        # if a token doesn't exists return to homepage
        return render(request, 'urls/home.html')


def myAdmin(request):
    try:
        # if a token exists return data
        if request.user.auth_token is not None:
            if request.user.is_superuser:
                # historias = Historia.objects.all()
                # return render(request, 'urls/index.html', {'historias': historias})
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

                # auth = authenticate(form.cleaned_data['username'], form.cleaned_data['password'])
                # token, _ = Token.objects.get_or_create(user=auth)
                # if token:
                #    login(request, user)

                # return redirect("index")
                # 1 = state
                # render(request, 'urls/register.html', {'state': '1'})
                return HttpResponseRedirect(reverse_lazy('index'))

    form = NewUserForm()
    return render(request, 'urls/register.html', {'register_form': form})

# Renderizar información de la historia
def infoHistoria(request, route):
    try:
        story = Story.objects.get(route=route)
        paginas = Page.objects.filter(story=story.id)
        has_pages = False
        if len(paginas) > 0:
            has_pages = True
        args = {'story': story, 'has_pages': has_pages}
    except:
        return HttpResponseNotFound()
    return render(request, 'urls/info_historia.html', args)


def contenidoHistoria(request, route, num_pagina):
    try:
        story = Story.objects.get(route=route)
        paginas = Page.objects.filter(story=story.id)
        continua = True
        if num_pagina >= len(paginas):
            continua = False
        pagina = paginas[num_pagina - 1]
        prueba = '<a href="https://www.google.com">Elemento a</a><div class="rojo">Elemento div</div>'
        args = {'story': story, 'pagina': pagina, 'continua': continua,
                'route': route, 'num_pagina': num_pagina + 1, 'prueba': prueba}
    except:
        return HttpResponseNotFound()

    return render(request, 'urls/contenido_historia.html', args)

