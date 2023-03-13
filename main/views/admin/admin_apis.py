import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict

from main.models import Story, UserProfile

from main.utils.ub_recommender import UserBasedRecommender


def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def updateUBRecommender(request):
    
    ubr = UserBasedRecommender()
    print('\n\n')
    #ubr.train()
    ubr.recommend(1, max_recommendations=6)
    print('\n\n')

    return JsonResponse({'message': 'success'})
