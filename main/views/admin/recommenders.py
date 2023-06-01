from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from main.utils.cb_recommender import ContentBasedRecommender
from main.utils.ub_recommender import UserBasedRecommender
from main.models import CBRSettings, UBRSettings

def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def index(request):
    if request.method == "GET":
        ubr_settings = UBRSettings.objects.first()
        cbr_settings = CBRSettings.objects.first()
        
        context = {
            'ubr_settings': ubr_settings,
            'cbr_settings': cbr_settings
        }
        
        return render(request, 'admin/recommenders.html', context=context)

# Content based recommender
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def cbrUpdateSettings(request):
    if request.method == 'POST':
        timeout = request.POST.get('timeout', 0)
        update = request.POST.get('update') == 'on'

        recommender_settings = CBRSettings.objects.first()
        if recommender_settings:
            recommender_settings.timeout = timeout
            recommender_settings.update_on_alter_stories = update
            # Update object
            recommender_settings.save()
            # Update cache server
            recommender = ContentBasedRecommender()
            recommender.update_timeout()
            # success
            return redirect('recommenders')
        else:
            # error
            return redirect('recommenders')


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def updateCBRecommender(request):
    if request.method == 'POST':
        cbr = ContentBasedRecommender()
        if cbr.train():
            return JsonResponse({'message': 'success'})


# User based recommender
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def ubrUpdateSettings(request):
    if request.method == 'POST':    
        timeout = request.POST.get('timeout', 0)

        recommender_settings = UBRSettings.objects.first()
        if recommender_settings:
            recommender_settings.timeout = timeout
            # Update object
            recommender_settings.save()
            # Update cache server
            recommender = UserBasedRecommender()
            recommender.update_timeout()
            # success
            return redirect('recommenders')
        else:
            # error
            return redirect('recommenders')
    

@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def updateUBRecommender(request):
    if request.method == 'POST':
        ubr = UserBasedRecommender()
        if ubr.train():
            return JsonResponse({'message': 'success'})