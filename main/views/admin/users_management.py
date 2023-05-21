import json

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict

from main.models import Story, UserProfile

from main.utils.cb_recommender import ContentBasedRecommender
from main.utils.ub_recommender import UserBasedRecommender


def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def delete(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        if user:
            if request.user.id == user.id:
                return JsonResponse({'message': 'You can\'t delete your own user'})
            user.delete()
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message:' 'not found'})


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def update(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        if user:
            if request.user.id == user.id:
                #return JsonResponse({'message': 'You can\'t edit your own user'})
                return redirect('index_admin')

            email = request.POST.get('email')
            is_superuser = request.POST.get('is_superuser') == 'on'
            is_staff = request.POST.get('is_staff') == 'on'

            if email=='':
                #return JsonResponse({'message': 'An email is required'})
                return redirect('index_admin')

            user.email = email
            user.is_superuser = is_superuser
            user.is_staff = is_staff
            user.save()

            return redirect('index_admin')