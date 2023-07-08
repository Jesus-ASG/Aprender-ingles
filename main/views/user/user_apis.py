from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Story, UserAnswer


@login_required(login_url='/login/')
def likeStory(request, story_id):
    if request.method == 'POST':
        key = f'user_likes_{request.user.id}'
        rate_limit = 150
        rate_limit_time = 60

        num_requests = cache.get(key, 0)
        if num_requests > rate_limit:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
        cache.set(key, num_requests + 1, rate_limit_time)

        user_profile = request.user.profile
        story = Story.objects.get(id=story_id)
        
        if story in user_profile.liked_stories.all():
            user_profile.liked_stories.remove(story)
            story.likes_number -= 1
        else:
            user_profile.liked_stories.add(story)
            story.likes_number += 1

        user_profile.save()
        story.save()
        return JsonResponse({'success': True})


@login_required(login_url='/login/')
def saveStory(request, story_id):
    if request.method == 'POST':
        key = f'user_saves_{request.user.id}'
        rate_limit = 150
        rate_limit_time = 60

        num_requests = cache.get(key, 0)
        if num_requests > rate_limit:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
        cache.set(key, num_requests + 1, rate_limit_time)

        user_profile = request.user.profile
        story = Story.objects.get(id=story_id)
        
        if story in user_profile.saved_stories.all():
            user_profile.saved_stories.remove(story)
        else:
            user_profile.saved_stories.add(story)

        user_profile.save()
        
        return JsonResponse({'success': True})


@login_required(login_url='/login/')
def deleteAnswers(request, story_id):
    #if request.method == 'POST':
    profile = request.user.profile
    story = Story.objects.get(pk=story_id)
    story_answers = UserAnswer.objects.filter(user_profile=profile, story=story)
    story_answers.delete()

    return JsonResponse({'message': 'success', 'action': 'story answers objects deleted'})
