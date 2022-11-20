
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from main.models import Story

def index(request, route):
    try:
        story = Story.objects.get(route=route)
        pages = story.pages.all()
    except:
        return HttpResponseNotFound()
    return render(request, 'admin/page-components/view-pages.html', {'story':story, 'pages':pages})

def create(request, route, id):
    try:
        story = Story.objects.get(route=route)
        pages = story.pages.all()
    except:
        return HttpResponseNotFound()
    match id:
        case 1:
            return render(request, 'admin/page-components/options/1.html', {'story':story, 'pages':pages})
    return redirect('view_pages', route=route)
