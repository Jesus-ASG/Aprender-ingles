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
            return redirect(reverse('flashcards_collections'))
        
        description = request.POST.get('description')
        FlashcardCollection.objects.create(
            user_profile=request.user.profile,
            collection_name=collection_name,
            description=description,
        )

        return redirect(reverse('flashcards_collections'))


def delete(request, fc_collection_id):
    if request.method == 'POST':
        try:
            collection = FlashcardCollection.objects.get(pk=fc_collection_id)
            collection.delete()
            return JsonResponse({'message': 'success'})
        except:
            return JsonResponse({'message': 'error'})


def update(request, fc_collection_id):
    if request.method == 'POST':
        collection = FlashcardCollection.objects.get(pk=fc_collection_id)

        collection_name = request.POST.get('collection_name')
        if collection_name == '':
            return redirect(reverse('flashcards_collections'))
        
        description = request.POST.get('description')

        collection.collection_name = collection_name
        collection.description = description
        collection.save()

        return redirect(reverse('flashcards_collections'))