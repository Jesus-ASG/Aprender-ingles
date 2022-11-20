# Historias
import re
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from main.forms import HistoriaForm, PaginaForm
from main.models import Story

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


def index(request):
    historias = Story.objects.all()
    return render(request, 'admin/historias/ver_historias.html', {'historias': historias})


def create(request):
    historiaFR = HistoriaForm(request.POST or None, request.FILES or None)
    paginaFR = PaginaForm(request.POST or None)

    if not historiaFR.is_valid():
        return render(request, 'admin/historias/agregar_historias.html',
                      {'formulario': historiaFR, 'form_pagina': paginaFR})

    historiaFO = historiaFR.save(commit=False)
    historiaFO.title = re.sub(' +', ' ', historiaFO.title)

    try:
        duplicado = Story.objects.get(title=historiaFO.title)
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
    """
    # old code for save many pages
    if paginaFR.is_valid():
        num_paginas = int(request.POST.get('num_paginas'))
        for i in range(num_paginas):
            texto = request.POST.get('texto_' + str(i))
            paginaFO = paginaFR.save(commit=False)
            paginaFO.texto = texto
            paginaFO.story = historiaFO
            paginaFO.save()
            paginaFR = PaginaForm()

        return redirect('ver_historias')
    """

def update(request, id):
    historia = Story.objects.get(id=id)
    # obtiene portada y ruta del objeto
    port1 = historia.get_portada()
    first_title = re.sub(' +', ' ', historia.title)

    fR = HistoriaForm(request.POST or None, request.FILES or None, instance=historia)
    if fR.is_valid() and request.POST:
        #### Cambiar ruta si es que modificó el título, ya que la ruta se basa en el título ####
        historia.title = re.sub(' +', ' ', historia.title)
        if first_title != historia.title:
            try:
                duplicado = Story.objects.get(title=historia.title)
                if duplicado:
                    resp = RespAlert()
                    resp.setAlert('danger')
                    resp.setMessage('Ya existe una historia con ese título')
                    return render(request, 'admin/historias/agregar_historias.html',
                                  {'formulario': fR, 'form_pagina': fR, 'resp': resp})
            except:
                # does nothing because save() method already save slug
                pass
        #### Portada ####
        # obtiene la portada del formulario
        port2 = historia.get_portada()
        # si las portadas son diferentes, entonces borra la anterior
        if port1 != port2:
            historia.del_portada(port1)
        fR.save()
        return redirect('ver_historias')
    return render(request, 'admin/historias/editar_historia.html', {'formulario': fR})


def delete(request, id):
    try:
        historia = Story.objects.get(id=id)
        historia.delete()
        return redirect('ver_historias')
    except:
        return HttpResponseBadRequest('')