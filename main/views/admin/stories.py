# Historias
import re
from django import forms
from django.utils.text import slugify

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render

from main.forms import HistoriaForm, PageForm
from main.models import Story, Tag

from main.utils.recommender import Recommender


def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def index(request):
    stories = Story.objects.all()
    tags = Tag.objects.all()
    context = {
        'stories': stories,
        'tags': tags,
    }
    return render(request, 'admin/index_admin.html', context)


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def create(request):
    action_type = 'Make a new story'
    storyF = HistoriaForm()
    context = {
        'action_type': action_type,
        'story_form': storyF,
    }

    if request.method == 'GET':
        return render(request, 'admin/story_form.html', context)
    
    if request.method == 'POST':
        storyF = HistoriaForm(request.POST or None, request.FILES or None)
        context['story_form'] = storyF
        if not storyF.is_valid():
            return render(request, 'admin/story_form.html', context)
        
        # check if title is not repeated
        story_obj = storyF.save(commit=False)
        story_obj.title1 = re.sub(' +', ' ', story_obj.title1)
        title_s = slugify(story_obj.title1)
        max_stories = Story.objects.filter(route=title_s).count()
        if max_stories > 0:
            context["error"] = "Ya existe una historia con ese título"
            return render(request, 'admin/story_form.html', context)
        storyF.save()

        recommender = Recommender()
        recommender.train()
        return redirect('view_pages', route=story_obj.route)


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def update(request, story_id):
    try:
        story = Story.objects.get(id=story_id)
    except:
        return HttpResponseNotFound()
    
    action_type = 'Edit story'
    storyF = HistoriaForm(instance=story)
    context = {
        'action_type': action_type,
        'story_form': storyF,
        'story': story,
    }
    if request.method == 'GET':
        return render(request, 'admin/story_form.html', context)
    
    if request.method == 'POST':
        storyF = HistoriaForm(request.POST or None, request.FILES or None, instance=story)
        context["story_form"] = storyF
        if not storyF.is_valid():
            return render(request, 'admin/story_form.html', context)
        
        # check if title is not repeated
        story.title1 = re.sub(' +', ' ', story.title1)
        title_s = slugify(story.title1)
        max_stories = Story.objects.filter(route=title_s).exclude(id=story_id).count()
        if max_stories > 0:
            context["error"] = "Ya existe una historia con ese título"
            return render(request, 'admin/story_form.html', context)
        storyF.save()
        recommender = Recommender()
        recommender.train()
        return redirect('index_admin')
        

@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def delete(request, story_id):
    try:
        historia = Story.objects.get(id=story_id)
        historia.delete()
        recommender = Recommender()
        recommender.train()
        return redirect('index_admin')
    except:
        return HttpResponseBadRequest('')