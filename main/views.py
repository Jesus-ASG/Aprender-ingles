from http.client import HTTPResponse
from django.shortcuts import render

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


class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication,)

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
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token, _ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)

class Logout(APIView):
    def get(self, request, format = None):
        # if a token auth exists, leave session and delete token
        try:
            if request.user.auth_token is not None:
                request.user.auth_token.delete()
                logout(request)
                return HttpResponseRedirect(reverse_lazy('login'))
        except AttributeError:
            # if there aren't a token send 404 not found
            return HttpResponseNotFound('')
    


def index(request):
    #aux = Logout()
    # if nobody is authenticated send to main page
    #if request.auth is None:
    #    return render(request, 'urls/index.html')
    # if somebody is authenticated send user's data and profile
    return render(request, 'urls/home.html')

# def login(request):
#     return render(request, 'urls/login.html')

def sign_in(request):
    return render(request, 'urls/sign_in.html')