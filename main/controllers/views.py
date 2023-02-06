from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Story


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'no-logged/home.html')
    
    page_title = 'Stories Gallery'
    stories = Story.objects.all()
    context = {
        'stories': stories,
        'page_title': page_title,
    }
    return render(request, 'user/index_user.html', context)
    

@login_required(login_url='/login/')
def savedStories(request):
    user_profile = request.user.profile
    page_title = 'Your saved stories'
    stories = Story.objects.filter(savedstory__user_profile=user_profile).order_by('-savedstory__date')

    context = {
        'page_title': page_title,
        'stories': stories,
    }
    return render(request, 'user/index_user.html', context)

