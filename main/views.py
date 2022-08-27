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
from django.http import HttpResponseRedirect
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
    success_url = reverse_lazy('main:users_list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            #####
            ###
            ####
            print('else dispatch')
            return super(Login, self).dispatch(request, *args, *kwargs)
    
    def form_valid(self, form):
        print('form valid excecuted')
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token, _ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)

class Logout(APIView):
    def get(self, request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)


def index(request):
    return render(request, 'urls/index.html')

# def login(request):
#     return render(request, 'urls/login.html')

def sign_in(request):
    return render(request, 'urls/sign_in.html')