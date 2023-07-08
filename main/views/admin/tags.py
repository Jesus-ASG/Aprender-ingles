from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import redirect, render

from main.forms import CategoriaForm
from main.models import Tag


def is_staff(user):
    return user.is_staff


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def index(request):
    if request.method == 'GET':
        tags = Tag.objects.all().order_by('name1')
        context = {
            'tags': tags
        }
        return render(request, 'admin/tags.html', context)


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def create(request):
    tagF = CategoriaForm()
    
    if request.method == 'POST':
        tagF = CategoriaForm(request.POST or None)
        if not tagF.is_valid():
            return redirect('tags')
        
        tagF.save()
        return redirect('tags')


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def update(request, tag_id):
    if request.method == 'POST':
        tag = Tag.objects.get(id=tag_id)
        if tag:
            tagF = CategoriaForm(instance=tag)
        
            tagF = CategoriaForm(request.POST or None, instance=tag)
            if not tagF.is_valid():
                return redirect('tags')
            
            tagF.save()
            return redirect('tags')


@login_required(login_url='/login/')
@user_passes_test(is_staff, login_url='/login/')
def delete(request, tag_id):
    if request.method == 'POST':
        tag = Tag.objects.get(id=tag_id)
        if tag:
            tag.delete()
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message:' 'not found'})

