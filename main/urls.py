from django.urls import path
from . import vistas as v
from main.controllers.admin import pages, tags, stories

# para cargar imagenes
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', v.index, name='index'),
    path('myadmin/', v.myAdmin, name='index_admin'),

    # Todas las historias y sus funciones
    path('myadmin/ver-historias', stories.index, name = 'ver_historias'),
    path('myadmin/agregar-historias', stories.create, name = 'agregar_historias'),
    path('myadmin/editar-historia/<int:id>', stories.update, name = 'editar_historia'),
    path('myadmin/eliminar-historia/<int:id>', stories.delete, name = 'eliminar_historia'),

    path('myadmin/view-pages/<slug:route>', pages.index, name='view_pages'),
    path('myadmin/view-pages/<slug:route>/add/<int:id>', pages.create, name='add_page'),
    path('myadmin/view-pages/del/', pages.delete, name='del_page'),

    # for stories and related
    path('historia/<slug:route>/', v.infoHistoria, name = 'info_historia'),
    path('historia/<slug:route>/<int:num_pagina>/', v.contenidoHistoria, name='contenido_historia'),
    
    #path('historia/agregar-pagina/<slug:route>', views.contenidoHistoria, name='contenido_historia'),

    # Todas las categorías y sus funciones
    path('myadmin/ver-categorias', tags.index, name = 'ver_categorias'),
    path('myadmin/agregar-categorias', tags.create, name = 'agregar_categorias'),
    path('myadmin/editar-categoria/<int:id>', tags.update, name = 'editar_categoria'),
    path('myadmin/eliminar-categoria/<int:id>', tags.delete, name = 'eliminar_categoria'),
    
    path('register', v.register, name='register'),
    path('user/', v.UsersList.as_view(), name = 'users_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)