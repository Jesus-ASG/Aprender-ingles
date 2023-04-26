import json

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict

from main.models import FlashcardCollection, Flashcard
from main.forms import ScoreForm, UserAnswer



@login_required(login_url='/login/')
def index(request):
    profile = request.user.profile
    flashcards_collections = FlashcardCollection.objects.filter(user_profile=profile)

    if request.method == 'GET':
        context = {
            'flashcards_collections': flashcards_collections
        }

        return render(request, 'user/flashcards.html', context)


@login_required(login_url='/login/')
def create(request):
    if request.method == 'POST':
        collection_name = request.POST.get('collection_name')
        if collection_name == '':
            return redirect(reverse('flashcards'))
        
        description = request.POST.get('description')
        FlashcardCollection.objects.create(
            user_profile=request.user.profile,
            collection_name=collection_name,
            description=description,
        )

        return redirect(reverse('flashcards'))
