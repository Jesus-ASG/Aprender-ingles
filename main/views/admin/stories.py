# Historias
import re
from django.utils.text import slugify

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render

from main.forms import HistoriaForm
from main.models import Story, Tag

from main.utils.cb_recommender import ContentBasedRecommender
from main.utils.paginate_and_filter import paginate_stories


def is_staff(user):
    return user.is_staff


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def index(request):
    q_items = request.GET.get('items_number')
    items_per_page = 5
    if q_items:
        try:
            q_items = int(q_items)
            if q_items > 0:
                items_per_page = q_items
        except:
            pass
    context = paginate_stories(request, items_per_page=items_per_page)
    context['filter_form']['items_number'] = items_per_page

    users = User.objects.exclude(id=request.user.id).values('id', 'username', 'email', 'is_staff', 'is_superuser')
    context['users'] = [request.user] + list(users)

    return render(request, 'admin/stories.html', context)


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def create(request):
    action_type = 'Agregar historia'
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

        recommender = ContentBasedRecommender()
        recommender.train()
        return redirect('view_pages', route=story_obj.route)


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def update(request, story_id):
    try:
        story = Story.objects.get(id=story_id)
    except:
        return HttpResponseNotFound()
    
    action_type = 'Editar historia'
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
        recommender = ContentBasedRecommender()
        recommender.train()
        return redirect('admin_stories')
        

@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def delete(request, story_id):
    try:
        historia = Story.objects.get(id=story_id)
        historia.delete()
        recommender = ContentBasedRecommender()
        recommender.train()
        return redirect('admin_stories')
    except:
        return HttpResponseBadRequest('')