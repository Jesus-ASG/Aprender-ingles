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
def index(request, fc_collection_id):
    # Check if owns the flashcard
    profile = request.user.profile
    fc_collection = FlashcardCollection.objects.get(pk=fc_collection_id)
    has_collection = profile.flashcards_collections.filter(pk=fc_collection.id).exists()
    if not has_collection:
        return redirect(reverse('flashcards_collections'))

    flashcards = fc_collection.flashcards.order_by('-updated_at')

    if request.method == 'GET':
        context = {
            'fc_collection': fc_collection,
            'flashcards': flashcards,
        }
        return render(request, 'user/flashcards.html', context)


@login_required(login_url='/login/')
def create(request, fc_collection_id):
    if request.method == 'POST':
        # Check if owns the flashcard
        profile = request.user.profile
        fc_collection = FlashcardCollection.objects.get(pk=fc_collection_id)
        has_collection = profile.flashcards_collections.filter(pk=fc_collection.id).exists()
        if not has_collection:
            return redirect(reverse('flashcards_collections'))

        # Save flashcard
        front = request.POST.get('front')
        if front == '':
            return redirect(reverse('flashcards_collections'))
        
        back = request.POST.get('back')
        color = request.POST.get('color')

        #print(f'\n{front}\n{back}\n{color}\n')
        
        Flashcard.objects.create(
            flashcard_collection=fc_collection,
            front=front,
            back=back,
            color=color,
        )
        return redirect(reverse('flashcards', args=[fc_collection_id]))


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