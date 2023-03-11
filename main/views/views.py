import json

from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from ..models import Story, Tag

stories_per_page = 8

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'no-logged/home.html')
    if request.method == 'GET':
        page_title = 'Recommended'
        message_if_empty = ''
        stories = Story.objects.all()

        context = {
            'page_title': page_title,
            'message_if_empty': message_if_empty,
            'stories': stories,
        }
        
        return render(request, 'user/index_user.html', context=context)


@login_required(login_url='/login/')
def storiesGallery(request):    
    if request.method == 'GET':
        # Get query params
        q_search = request.GET.get('s')
        q_tags = request.GET.getlist('tag')
        q_sort_date = request.GET.get('sort_date')
        q_sort_name = request.GET.get('sort_name')
        q_page = request.GET.get('p')

        filter_form = {
            's': q_search,
            'tags': q_tags,
            'sort_date': q_sort_date,
            'sort_name': q_sort_name
        }
        
        user_profile = request.user.profile
        page_title = 'Stories Gallery'
        message_if_empty = ''
        stories = Story.objects.all().exclude(xp_required__gt = user_profile.xp).order_by('title1')
        tags = Tag.objects.all().order_by('name1')
        
        # Custom filters
        # Sort by name
        if not q_sort_name == 'default':
            if q_sort_name == 'a-z':
                stories = stories.order_by('title1')
            elif q_sort_name == 'z-a':
                stories = stories.order_by('-title1')
        
        # Search
        if q_search:
            stories = stories.filter(Q(title1__icontains=q_search) | Q(title2__icontains=q_search))

        # Filter by tags
        try:
            if not q_tags[0] == 'all':
                q_tag_ids = [int(x) for x in q_tags]    
                stories = stories.filter(tags__id__in=q_tag_ids).distinct()
        except:
            pass

        # Sort by date
        if not q_sort_date == 'default':
            if q_sort_date == 'updated':
                stories = stories.order_by('-updated_at')
            elif q_sort_date == 'created':
                stories = stories.order_by('-created_at')


        # Paginate        
        paginator = Paginator(stories, 8)
        try:
            q_page = int(q_page)
            if q_page <=0:
                q_page = 1
            if q_page > paginator.num_pages:
                q_page = paginator.num_pages
        except:
            q_page = 1


        elided_page_range = list(paginator.get_elided_page_range(q_page, on_each_side=2, on_ends=1))

        query_params = request.GET.copy()
        page_range = []
        for p in elided_page_range:
            if type(p) == int:
                query_params['p'] = p
                url = '{}?{}'.format(request.path, query_params.urlencode())
            else:
                url = '#'
            page_range.append({'label': p, 'url': url})
        
        
        stories = paginator.page(q_page)
        urls = {}
        query_params = request.GET.copy()

        if stories.has_previous():
            query_params['p'] = stories.previous_page_number()
            urls['prev'] = '{}?{}'.format(request.path, query_params.urlencode())

        if stories.has_next():
            query_params['p'] = stories.next_page_number()
            urls['next'] = '{}?{}'.format(request.path, query_params.urlencode())
        
        
        #print(f'\nPrev:{stories.has_previous()}\nNext:{stories.has_next()}\n')

        context = {
            'page_title': page_title,
            'stories': stories,
            'tags': tags,
            'filter_form': filter_form,
            'page_range': page_range,
            'urls': urls,
            'message_if_empty': message_if_empty,
        }
        return render(request, 'user/stories_gallery.html', context)
    

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

