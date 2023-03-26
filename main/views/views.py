from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Subquery, OuterRef, Max
from django.http import HttpResponseNotFound

from main.models import Story, Tag, UserProfile, Score
from main.forms import SelectDefaultImageForm

from main.utils.ub_recommender import UserBasedRecommender
from main.utils.level_manager import LevelManager
from main.utils.evaluate_story import rateSkills
from main.utils.paginate_and_filter import paginate_stories


def not_found_page(request, exception):
    return render(request, 'utils/404_page.html', {})

def test_not_found(request):
    return render(request, 'utils/404_page.html', {})

def index(request):
    
    if not request.user.is_authenticated:
        return render(request, 'no-logged/home.html')
    if request.method == 'GET':
        page_title = 'Recommended'
        message_if_empty = ''
        ubr = UserBasedRecommender()
        user_profile = request.user.profile
        stories = ubr.recommend(user_profile.id, max_recommendations=6)
        #print(user_profile.id)
        #stories = Story.objects.all()
        context = {
            'page_title': page_title,
            'message_if_empty': message_if_empty,
            'stories': stories,
        }
        
        return render(request, 'user/index_user.html', context=context)


@login_required(login_url='/login/')
def profile(request):

    profile = request.user.profile
    default_image_form = SelectDefaultImageForm(instance=profile)

    lvl_obj = LevelManager()
    level_statistics = lvl_obj.get_level_statistics(profile.xp)

    statistics = {
        'level': level_statistics
    }

    context = {
        'profile': profile,
        'statistics': statistics,
        'default_image_form': default_image_form
    }

    if request.method == 'GET':
        max_scores = Score.objects.filter(user_profile=profile).values('story').annotate(max_score_percentage=Max('score_percentage'))
        
        subquery = max_scores.filter(story=OuterRef('story')).values('max_score_percentage')
        user_scores = Score.objects.filter(user_profile=profile, score_percentage__in=Subquery(subquery))

        # Uniques high scores
        u_high_scores = []
        user_scores = user_scores.order_by('-score_percentage', 'date')
        for i in user_scores:
            if not i.story in [x['score'].story for x in u_high_scores]:
                grade = rateSkills(i.score_percentage)
                u_high_scores.append({'score': i, 'grade': grade})

        wa = 0
        ca = 0
        sa = 0
        for i in u_high_scores:
            wa += i['score'].writing_percentage
            ca += i['score'].comprehension_percentage
            sa += i['score'].speaking_percentage
        num_elements = 1 if len(u_high_scores) <= 0 else len(u_high_scores)
        wa = wa / num_elements
        ca = ca / num_elements
        sa = sa / num_elements

        wg = rateSkills(wa)
        cg = rateSkills(ca)
        sg = rateSkills(sa)
        
        context['statistics']['writing'] = { 'average': wa, 'grade':wg }
        context['statistics']['comprehension'] = { 'average': ca, 'grade':cg }
        context['statistics']['speaking'] = { 'average': sa, 'grade':sg }
        
        context['u_high_scores'] = u_high_scores

        return render(request, 'user/profile.html', context)
    
    if request.method == 'POST':
        default_image_form = SelectDefaultImageForm(request.POST or None)
        if not default_image_form.is_valid():
            return render(request, 'user/profile.html', context)
        
        profile_obj = UserProfile.objects.get(user=request.user)
        profile_obj.default_profile_image = default_image_form.cleaned_data['default_profile_image']
        profile_obj.save()
        
        #context['success'] = True
        # Update
        return redirect('profile')
        #return render(request, 'user/profile.html', context)


@login_required(login_url='/login/')
def storiesList(request):
    if request.method == 'GET':

        context = paginate_stories(request, items_per_page=8)
        
        return render(request, 'user/stories_gallery.html', context)

