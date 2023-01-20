
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from main.models import Story, Page, Image, Dialogue, RepeatPhrase
from main.forms import DialogueForm, ImageForm, PageForm, RepeatPhraseForm

from django.core import serializers
from django.forms.models import model_to_dict

import json

MAX_PAGE_TYPES = 1

def index(request, route):
    try:
        story = Story.objects.get(route=route)
        pages = story.pages.all().order_by('date_created', 'time_created').values()
    except:
        return HttpResponseNotFound()
    return render(request, 'admin/page-components/view-pages.html', {'story':story, 'pages':pages})


def create(request, route, page_type):
    if not 0 < page_type <= MAX_PAGE_TYPES:
        return HttpResponseNotFound()
    try:
        story = Story.objects.get(route=route)
    except:
        return HttpResponseNotFound()

    if request.method == "GET":
        return render(request, 'admin/page-components/options/'+str(page_type)+'.html', 
        {'story': story, 'page_type': page_type})

    if request.method == "POST":
        if page_type == 0:
            return HttpResponseNotFound()
        
        # create all forms
        pgForm = PageForm(request.POST or None)
        imgForm = ImageForm(request.POST or None, request.FILES or None)
        diaForm = DialogueForm(request.POST or None)
        repPForm = RepeatPhraseForm(request.POST or None)

        # validation
        if ((not pgForm.is_valid()) or (not imgForm.is_valid()) or (not diaForm.is_valid()) or 
                (not repPForm.is_valid())):
            return JsonResponse({'message': 'error validating'})

        # collecting data
        data = request.POST["data"]
        data = json.loads(data)
        
        #print(f'\n\n{data}\n\n')
        #print(f'\n\n{objects_deleted}\n\n')

        # creating page
        pgObj = pgForm.save(commit=False)
        if data["page_id"] != "":
            pgObj = Page.objects.get(id=int(data["page_id"]))
        
        pgObj.story = story
        pgObj.subtitle1 = data["sub1"]
        pgObj.subtitle2 = data["sub2"]
        pgObj.page_type = page_type
        
        
        # saving images
        images_to_submit = []
        imageFiles = request.FILES.getlist("imageFiles[]")
        imageData = data["imageData"]
        for imgF, imgD in zip (imageFiles, imageData):
            imgObj = imgForm.save(commit=False)
            if imgD["id"] != "":
                imgObj = Image.objects.get(id=int(imgD["id"]))
            imgObj.page = pgObj
            imgObj.image = imgF
            imgObj.element_number = imgD["element_number"]
            images_to_submit.append(imgObj)
            imgForm = ImageForm(request.POST or None, request.FILES or None)
        
        # saving dialogs
        dialogues_to_submit = []
        dialogues = data["dialogues"]
        for d in dialogues:
            if d["name"] == "" or d["language1"] == "" or d["language2"] == "":
                return JsonResponse({'message': 'error catched in for'})
            
            diaObj = diaForm.save(commit=False)
            if d["id"] != "":
                diaObj = Dialogue.objects.get(id=int(d["id"]))
            diaObj.page = pgObj
            diaObj.name = d["name"]
            diaObj.content1 = d["language1"]
            diaObj.content2 = d["language2"]
            diaObj.color = d["color"]
            diaObj.element_number = d["element_number"]
            dialogues_to_submit.append(diaObj)
            diaForm = DialogueForm(request.POST or None)
        
        # saving repeatPhrases
        repeatPhrases_to_submit = []
        repeatPhrases = data["repeatPhrases"]
        for rp in repeatPhrases:
            if rp["language1"] == "" or rp["language2"] == "":
                return JsonResponse({'message': 'error catched in for'})
            
            rpPObj = repPForm.save(commit=False)
            if rp["id"] != "":
                rpPObj = RepeatPhrase.objects.get(id=int(rp["id"]))
            rpPObj.page = pgObj
            rpPObj.content1 = rp["language1"]
            rpPObj.content2 = rp["language2"]
            rpPObj.element_number = rp["element_number"]
            repeatPhrases_to_submit.append(rpPObj)
            repPForm = RepeatPhraseForm(request.POST or None)    
        

        # Delete objects that were deleted
        deleted = data["deleted"]
        deleted_dialogues = deleted["dialogues"]
        for d in deleted_dialogues:
            try:
                Dialogue.objects.get(id=int(d)).delete()
            except:
                pass
        
        deleted_repeatPhrases = deleted["repeatPhrases"]
        for d in deleted_repeatPhrases:
            try:
                RepeatPhrase.objects.get(id=int(d)).delete()
            except:
                pass

        
        # Save all
        pgObj.save()
        
        # Content
        # Images
        for image in images_to_submit:
            image.save()
        
        # Dialogues
        for dialogue in dialogues_to_submit:
            dialogue.save()
        
        # Repeat Phrases
        for repeatPhrase in repeatPhrases_to_submit:
            repeatPhrase.save()
        
        return JsonResponse({'message': 'success'})
        

def update(request, route, page_type, page_id):
    if not 0 < page_type <= MAX_PAGE_TYPES:
        return HttpResponseNotFound()
    try:
        # get content
        story = Story.objects.get(route=route)
        page = story.pages.get(id=page_id)

        images = page.images.all()
        dialogues = page.dialogues.all()
        repeat_phrases = page.repeat_phrases.all()

        # get values from query set
        #page = model_to_dict(page)
        dialogues = list(dialogues.values())
        repeat_phrases = list(repeat_phrases.values())
        
        
        # cast list to json
        #page = json.dumps(page)
        dialogues = json.dumps(dialogues)
        repeat_phrases = json.dumps(repeat_phrases)

        # image different to get url image instead image
        # only if page_type != 1
        
        images_json = []
        for image in images:
            x = model_to_dict(image)
            x['image'] = x['image'].url
            images_json.append(x)
        images_json = json.dumps(images_json)

        context = {
            'story': story, 'page': page, 'page_type': page_type,
            'images': images, 'images_json': images_json, 'dialogues': dialogues, 
            'repeat_phrases': repeat_phrases
        }

        #print('\n\n')
        print(f'{page}\n\n{images}\n\n{images_json}\n\n{dialogues}\n\n{repeat_phrases}')
        #print('\n\n')

    except:
        
        return HttpResponseNotFound()
    
    if request.method == "GET":
        return render(request, 'admin/page-components/options/'+str(page_type)+'.html', context)


def delete(request, id):
    if request.method == "POST":
        try:
            page = Page.objects.get(id=id)
            page.delete()
            return HttpResponse(status=200)
        except:
            return HttpResponseBadRequest('')