from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from main.forms import CategoriaForm
from main.models import Tag


def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def create(request):
    action_type = 'Add a new tag'
    tagF = CategoriaForm()

    context = {
        'action_type':action_type,
        'tag_form': tagF,
    }

    if request.method == 'GET':
        return render(request, 'admin/tag_form.html', context)
    
    if request.method == 'POST':
        tagF = CategoriaForm(request.POST or None)
        if not tagF.is_valid():
            return render(request, 'admin/tag_form.html', context)
        
        tagF.save()
        return redirect('index_admin')


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def update(request, tag_id):
    try:
        tag = Tag.objects.get(id=tag_id)
    except:
        return HttpResponseNotFound()
    
    action_type = 'Edit tag'
    tagF = CategoriaForm(instance=tag)
    context = {
        'action_type':action_type,
        'tag_form': tagF,
    }

    if request.method == 'GET':
        return render(request, 'admin/tag_form.html', context)
    
    if request.method == 'POST':
        tagF = CategoriaForm(request.POST or None, instance=tag)
        context["tag_form"] = tagF
        if not tagF.is_valid():
            return render(request, 'admin/tag_form.html', context)
        
        tagF.save()
        return redirect('index_admin')


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def delete(request, tag_id):
    categoria = Tag.objects.get(id=tag_id)
    categoria.delete()
    return redirect('index_admin')