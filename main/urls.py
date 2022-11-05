from django.urls import path
from . import views

# para cargar imagenes
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.index, name='index'),
    path('myadmin/', views.myAdmin, name='index_admin'),

    # Todas las historias y sus funciones
    path('myadmin/ver-historias', views.verHistorias, name = 'ver_historias'),
    path('myadmin/agregar-historias', views.agregarHistorias, name = 'agregar_historias'),
    path('myadmin/editar-historia/<int:id>', views.editarHistoria, name = 'editar_historia'),
    path('myadmin/eliminar-historia/<int:id>', views.eliminarHistoria, name = 'eliminar_historia'),
    path('myadmin/edit-pages/<slug:route>', views.editPages, name='edit_pages'),

    # for stories and related
    path('historia/<slug:route>/', views.infoHistoria, name = 'info_historia'),
    path('historia/<slug:route>/<int:num_pagina>/', views.contenidoHistoria, name='contenido_historia'),
    
    #path('historia/agregar-pagina/<slug:route>', views.contenidoHistoria, name='contenido_historia'),

    # Todas las categorías y sus funciones
    path('myadmin/ver-categorias', views.verCategorias, name = 'ver_categorias'),
    path('myadmin/agregar-categorias', views.agregarCategorias, name = 'agregar_categorias'),
    path('myadmin/editar-categoria/<int:id>', views.editarCategoria, name = 'editar_categoria'),
    path('myadmin/eliminar-categoria/<int:id>', views.eliminarCategoria, name = 'eliminar_categoria'),
    
    path('register', views.register, name='register'),
    path('user/', views.UsersList.as_view(), name = 'users_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)