from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from main.forms import CategoriaForm
from main.models import Tag


def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def index(request):
    categorias = Tag.objects.all().order_by('name1')
    return render(request, 'admin/categorias/ver_categorias.html', {'categorias': categorias})


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def create(request):
    formulario = CategoriaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
    return render(request, 'admin/categorias/agregar_categorias.html', {'formulario': formulario})


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def update(request, id):
    categoria = Tag.objects.get(id=id)
    formulario = CategoriaForm(request.POST or None, instance=categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
    return render(request, 'admin/categorias/editar_categoria.html', {'formulario': formulario})


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def delete(request, id):
    categoria = Tag.objects.get(id=id)
    categoria.delete()
    return redirect('ver_categorias')