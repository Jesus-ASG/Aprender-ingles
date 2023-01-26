
from django.shortcuts import render, redirect

from rest_framework import generics
from .models import User
from .serializers import UserSerializer

from django.urls import reverse_lazy
from django.urls import reverse

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

import json

class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)


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
            print('rendering no-logged/index.html')
            return render(request, 'no-logged/index.html', {'historias': historias, 'user': user})
    except AttributeError:
        # if a token doesn't exists return to homepage
        return render(request, 'no-logged/home.html')


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
    return render(request, 'no-logged/register.html', {'register_form': form})

    