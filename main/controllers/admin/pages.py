
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from main.models import Story, Page, Image
from main.forms import DialogueForm, ImageForm, PageForm

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
        match id:
            case 1:
                cont = 0
                subtitle = request.POST.get('subtitle')
                pgForm = PageForm(request.POST or None)
                if not pgForm.is_valid():
                    return redirect('add_page', route=story.route, id=1)
                pgObj = pgForm.save(commit=False)
                pgObj.story = story
                pgObj.subtitle = subtitle
                pgObj.page_type = 1
                pgObj = pgForm.save()
                
                img_validation = request.POST.get('image')
                if img_validation != '':
                    imgForm = ImageForm(request.POST or None, request.FILES or None)
                    if imgForm.is_valid():
                        imgObj = imgForm.save(commit=False)
                        imgObj.page = pgObj
                        imgObj.image = request.FILES['image']
                        imgObj.element_number = 0
                        imgForm.save()
                
                
                max_elem = int(request.POST.get('max_elem'))
                if max_elem > 0:
                    for i in range(max_elem-2):
                        name = request.POST.get('name_'+str(i))
                        if name != None:
                            diaForm = DialogueForm(request.POST or None)
                            if diaForm.is_valid:
                                diaObj = diaForm.save(commit=False)
                                diaObj.page = pgObj
                                diaObj.name = request.POST.get('name_'+str(i))
                                diaObj.content = request.POST.get('content_'+str(i))
                                diaObj.content1 = request.POST.get('translation_' + str(i))
                                diaObj.color = request.POST.get('color_'+str(i))
                                diaObj.element_number = cont
                                diaForm.save()

                                cont = cont + 1
                                return redirect('view_pages', route=story.route)
        
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