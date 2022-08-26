from django.shortcuts import render

from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UsersList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def index(request):
    return render(request, 'urls/index.html')

def login(request):
    return render(request, 'urls/login.html')

def sign_in(request):
    return render(request, 'urls/sign_in.html')