import json

from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from ..models import Story

stories_per_page = 8

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'no-logged/home.html')
    
    if request.method == 'GET':
        # Get query params
        search = request.GET.get('search')
        page = request.GET.get('page')
        try:
            page = int(page)
        except:
            page = 1

        user_profile = request.user.profile
        page_title = 'Stories Gallery'
        message_if_empty = ''
        stories = Story.objects.all().exclude(xp_required__gt = user_profile.xp).order_by('title1')
        
        # Custom filters
        if search:
            stories = stories.filter(Q(title1__icontains=search) | Q(title2__icontains=search))

        # Paginate        
        paginator = Paginator(stories, 1)

        elided_page_range = list(paginator.get_elided_page_range(page, on_each_side=2, on_ends=1))
        
        query_params = request.GET.copy()
        page_range = []
        for p in elided_page_range:
            if type(p) == int:
                query_params['page'] = p
                url = '{}?{}'.format(request.path, query_params.urlencode())
            else:
                url = '#'
            page_range.append({'label': p, 'url': url})
        
        try:
            stories = paginator.page(page)
            urls = {}
            query_params = request.GET.copy()

            if stories.has_previous():
                query_params['page'] = stories.previous_page_number()
                urls['prev'] = '{}?{}'.format(request.path, query_params.urlencode())

            if stories.has_next():
                query_params['page'] = stories.next_page_number()
                urls['next'] = '{}?{}'.format(request.path, query_params.urlencode())

        except PageNotAnInteger:
            stories = paginator.page(1)
        except EmptyPage:
            stories = paginator.page(paginator.num_pages)
        
        #print(f'\nPrev:{stories.has_previous()}\nNext:{stories.has_next()}\n')

        context = {
            'stories': stories,
            'page_range': page_range,
            'urls': urls,
            'page_title': page_title,
            'message_if_empty': message_if_empty,
        }
        return render(request, 'user/index_user.html', context)
    

@login_required(login_url='/login/')
def savedStories(request):
    user_profile = request.user.profile
    page_title = 'Your saved stories'
    message_if_empty = "You don't have saved stories yet"
    stories = Story.objects.filter(savedstory__user_profile=user_profile).order_by('-savedstory__date')

    context = {
        'page_title': page_title,
        'stories': stories,
        'message_if_empty': message_if_empty,
    }
    return render(request, 'user/index_user.html', context)


@login_required(login_url='/login/')
def likedStories(request):
    user_profile = request.user.profile
    page_title = 'Your favorite stories'
    message_if_empty = "You don't have favorite stories yet"
    stories = Story.objects.filter(likedstory__user_profile=user_profile).order_by('-likedstory__date')

    context = {
        'page_title': page_title,
        'stories': stories,
        'message_if_empty': message_if_empty,
    }
    return render(request, 'user/index_user.html', context)

