import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from main.utils.cb_recommender import ContentBasedRecommender
from main.utils.ub_recommender import UserBasedRecommender
from main.models import AppSettings

def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def index(request):
    if request.method == "GET":
        ubr_settings = AppSettings.objects.filter(key='ubr').first()
        if ubr_settings:
            ubr_settings = json.loads(ubr_settings.value)

        cbr_settings = AppSettings.objects.filter(key='cbr').first()
        if cbr_settings:
            cbr_settings = json.loads(cbr_settings.value)
        
        context = {
            'ubr_settings': ubr_settings,
            'cbr_settings': cbr_settings
        }
        
        return render(request, 'admin/recommenders.html', context=context)

# Content based recommender
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def cbrSettings(request):
    if request.method == 'POST':
        timeout = request.POST.get('timeout', 0)
        update = request.POST.get('update') == 'on'

        cbr_obj = AppSettings.objects.filter(key='cbr').first()
        if cbr_obj:
            cbr_settings = json.loads(cbr_obj.value)
            cbr_settings['timeout'] = timeout
            cbr_settings['update_on_alter_stories'] = update

            cbr_settings = json.dumps(cbr_settings)
            cbr_obj.value = cbr_settings
            # Update object
            cbr_obj.save()
            # Update cache server
            cbr = ContentBasedRecommender()
            cbr.update_timeout()
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
def ubrSettings(request):
    if request.method == 'POST':    
        timeout = request.POST.get('timeout', 0)

        ubr_obj = AppSettings.objects.filter(key='ubr').first()
        if ubr_obj:
            ubr_settings = json.loads(ubr_obj.value)
            ubr_settings['timeout'] = timeout

            ubr_settings = json.dumps(ubr_settings)
            ubr_obj.value = ubr_settings
            # Update object
            ubr_obj.save()
            # Update cache server
            ubr = UserBasedRecommender()
            ubr.update_timeout()
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