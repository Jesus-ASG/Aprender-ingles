# Historias
import re

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from main.forms import HistoriaForm, PageForm
from main.models import Story


def is_superuser(user):
    return user.is_superuser


class RespAlert:
    def __init__(self):
        self.alert = ''
        self.message = ''

    def setAlert(self, alert):
        match alert:
            case 'danger':
                self.alert = 'alert-danger'

    def setMessage(self, message):
        self.message = message


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def index(request):
    stories = Story.objects.all()
    return render(request, 'admin/index1.html', {'stories': stories})


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def create(request):
    historiaFR = HistoriaForm(request.POST or None, request.FILES or None)
    paginaFR = PageForm(request.POST or None)

    if not historiaFR.is_valid():
        return render(request, 'admin/historias/agregar_historias.html',
                      {'formulario': historiaFR, 'form_pagina': paginaFR})

    historiaFO = historiaFR.save(commit=False)
    historiaFO.title1 = re.sub(' +', ' ', historiaFO.title1)

    try:
        duplicado = Story.objects.get(title=historiaFO.title1)
        if duplicado:
            resp = RespAlert()
            resp.setAlert('danger')
            resp.setMessage('Ya existe una historia con ese título')
            return render(request, 'admin/historias/agregar_historias.html',
                          {'formulario': historiaFR, 'form_pagina': paginaFR, 'resp': resp})
    except:
        # does nothing because save() method already save slug
        pass
    historiaFO = historiaFR.save()
    return redirect('view_pages', route=historiaFO.route)


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def update(request, id):
    historia = Story.objects.get(id=id)
    # obtiene portada y ruta del objeto
    port1 = historia.get_portada()
    first_title = re.sub(' +', ' ', historia.title1)

    fR = HistoriaForm(request.POST or None, request.FILES or None, instance=historia)
    if fR.is_valid() and request.POST:
        #### Cambiar ruta si es que modificó el título, ya que la ruta se basa en el título ####
        historia.title1 = re.sub(' +', ' ', historia.title1)
        if first_title != historia.title1:
            try:
                duplicado = Story.objects.get(title=historia.title1)
                if duplicado:
                    resp = RespAlert()
                    resp.setAlert('danger')
                    resp.setMessage('Ya existe una historia con ese título')
                    return render(request, 'admin/historias/agregar_historias.html',
                                  {'formulario': fR, 'form_pagina': fR, 'resp': resp})
            except:
                # does nothing because save() method already save slug
                pass

        fR.save()
        return redirect('ver_historias')
    return render(request, 'admin/historias/editar_historia.html', {'formulario': fR})


@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def delete(request, id):
    #if request.method == "POST":
    try:
        historia = Story.objects.get(id=id)
        historia.delete()
        return redirect('index_admin')
    except:
        return HttpResponseBadRequest('')