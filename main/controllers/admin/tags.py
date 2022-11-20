from django.shortcuts import redirect, render
from main.forms import CategoriaForm
from main.models import Tag


def index(request):
    categorias = Tag.objects.all().order_by('name')
    return render(request, 'admin/categorias/ver_categorias.html', {'categorias': categorias})


def create(request):
    formulario = CategoriaForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
    return render(request, 'admin/categorias/agregar_categorias.html', {'formulario': formulario})


def update(request, id):
    categoria = Tag.objects.get(id=id)
    formulario = CategoriaForm(request.POST or None, instance=categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
    return render(request, 'admin/categorias/editar_categoria.html', {'formulario': formulario})


def delete(request, id):
    categoria = Tag.objects.get(id=id)
    categoria.delete()
    return redirect('ver_categorias')