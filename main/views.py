from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'urls/index.html')

def login(request):
    return render(request, 'urls/login.html')

def sign_in(request):
    return render(request, 'urls/sign_in.html')