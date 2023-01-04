
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from main.models import Story, Page, Image
from main.forms import DialogueForm, ImageForm, PageForm

import json

def index(request, route):
    try:
        story = Story.objects.get(route=route)
        pages = story.pages.all().order_by('date_created', 'time_created').values()
    except:
        return HttpResponseNotFound()
    return render(request, 'admin/page-components/view-pages.html', {'story':story, 'pages':pages})


def create(request, route, id):
    try:
        story = Story.objects.get(route=route)
        pages = story.pages.all()
    except:
        return HttpResponseNotFound()

    if request.method == "POST":
        if id == 0:
            return HttpResponseNotFound()
        
        
        # create all forms
        pgForm = PageForm(request.POST or None)
        imgForm = ImageForm(request.POST or None, request.FILES or None)
        diaForm = DialogueForm(request.POST or None)

        # validation
        if (not pgForm.is_valid()) or (not imgForm.is_valid()) or (not diaForm.is_valid()):
            return JsonResponse({'message': 'error validating'})

        # collecting data
        data = request.POST["data"]
        data = json.loads(data)
        # creating page
        pgObj = pgForm.save(commit=False)
        pgObj.story = story
        pgObj.subtitle1 = data["sub1"]
        pgObj.subtitle2 = data["sub2"]
        pgObj.page_type = id
        
        # saving images
        images_to_submit = []
        imageFiles = request.FILES.getlist("imageFiles[]")
        imageData = data["imageData"]
        for imgF, imgD in zip (imageFiles, imageData):
            imgObj = imgForm.save(commit=False)
            imgObj.page = pgObj
            imgObj.image = imgF
            imgObj.element_number = imgD
            images_to_submit.append(imgObj)
            imgForm = ImageForm(request.POST or None, request.FILES or None)

        
        # saving dialogs
        dialogs_to_submit = []
        dialogs = data["dialogs"]
        for d in dialogs:
            if d["name"] == "" or d["language1"] == "" or d["language2"] == "":
                return JsonResponse({'message': 'error catched in for'})
            
            diaObj = diaForm.save(commit=False)
            diaObj.page = pgObj
            diaObj.name = d["name"]
            diaObj.content1 = d["language1"]
            diaObj.content2 = d["language2"]
            diaObj.color = d["color"]
            diaObj.element_number = d["element_number"]
            dialogs_to_submit.append(diaObj)
            diaForm = DialogueForm(request.POST or None)

            
            #return redirect('view_pages', route=story.route)
        
        # if comes until here means that dont have errors, so we save everything
        pgObj = pgForm.save()

        # save images if there are
        for image in images_to_submit:
            image.save()

        # save dialogues if there are
        for dialogue in dialogs_to_submit:
            dialogue.save()

        
        
        return JsonResponse({'message': 'success'})
        
    return render(request, 'admin/page-components/options/1.html', {'story':story, 'pages':pages})
    #return redirect('view_pages', route=route)


def delete(request):
    if request.method == "POST":
        try:
            pid = request.POST.get('pid')
            page = Page.objects.get(id=pid)
            page.delete()
            return HttpResponse(status=200)
        except:
            return HttpResponseBadRequest('')