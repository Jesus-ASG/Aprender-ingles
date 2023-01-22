import json
from django.shortcuts import render, redirect
# Renderizar información de la historia
from django.http import HttpResponseNotFound
from django.forms.models import model_to_dict

from main.models import Story


def storyInfo(request, route):
    try:
        story = Story.objects.get(route=route)
        pages = story.pages.all().order_by('date_created', 'time_created').values()
        next_page = None
        page_number = 0
        has_pages = True if len(pages) > 0 else False
        if (has_pages):
            next_page = pages[0]
        context = {
            'story': story, 
            'page_number': page_number,
            'has_pages': has_pages, 
            'next_page': next_page
            }
    except:
        return HttpResponseNotFound()
    return render(request, 'urls/story/story_info.html', context)


def storyContent(request, route, page_number):
    try:
        story = Story.objects.get(route=route)
        pages = story.pages.all().order_by('date_created', 'time_created')
        prev_page = None
        next_page = None
        current_page = pages[page_number]

        if page_number >= 1:
            prev_page = page_number - 1 
        if page_number < len(pages) - 1:
            next_page = page_number + 1
        
        images = current_page.images.all()
        dialogues = current_page.dialogues.all()
        repeat_phrases = current_page.repeat_phrases.all()

        dialogues = json.dumps(list(dialogues.values()))
        repeat_phrases = json.dumps(list(repeat_phrases.values()))

        images_json = []
        for image in images:
            x = model_to_dict(image)
            x['image'] = x['image'].url
            images_json.append(x)
        images_json = json.dumps(images_json)
        
        context = {
            'story': story,
            'page_number': page_number,
            'prev_page': prev_page,
            'next_page': next_page,
            'current_page': current_page,
            'images': images,
            'images_json': images_json,
            'dialogues': dialogues,
            'repeat_phrases': repeat_phrases
            }
    except:
        return HttpResponseNotFound()

    if request.method == "GET":
        return render(request, 'urls/story/story_content_'+str(current_page.page_type)+'.html', context)