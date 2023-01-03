
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
        page_type = 0
        match id:
            case 1:
                page_type = 1
            case 2:
                page_type = 2
        
        if page_type == 0:
            return HttpResponseNotFound()

        # validation
        pgForm = PageForm(request.POST or None)
        if not pgForm.is_valid():
            return redirect('add_page', route=story.route, id=page_type)

        # collecting data
        data = request.POST["data"]
        data = json.loads(data)
        # creating page
        pgObj = pgForm.save(commit=False)
        pgObj.story = story
        pgObj.subtitle = data["sub1"]
        pgObj.page_type = page_type
        pgObj = pgForm.save()
        
        # saving images
        imageFiles = request.FILES.getlist("imageFiles[]")
        imageData = data["imageData"]
        for imgF, imgD in zip (imageFiles, imageData):
            imgForm = ImageForm(request.POST or None, request.FILES or None)
            if imgForm.is_valid():
                imgObj = imgForm.save(commit=False)
                imgObj.page = pgObj
                imgObj.image = imgF
                imgObj.element_number = imgD
                imgForm.save()
        
        # saving dialogs
        dialogs = data["dialogs"]
        for d in dialogs:
            if d["name"] == "" or d["language1"] == "" or d["language2"] == "":
                return JsonResponse({'message': 'error'})
            diaForm = DialogueForm(request.POST or None)
            if diaForm.is_valid:
                diaObj = diaForm.save(commit=False)
                diaObj.page = pgObj
                diaObj.name = d["name"]
                diaObj.content = d["language1"]
                diaObj.content1 = d["language2"]
                diaObj.color = d["color"]
                diaObj.element_number = d["element_number"]
                diaForm.save()
                #return redirect('view_pages', route=story.route)
        
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