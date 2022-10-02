from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('myadmin', views.IndexAdmin.as_view(), name='index_admin'),
    path('myadmin/agregar-historias', views.agregarHistorias, name = 'agregar_historias'),
    
    path('myadmin/ver-categorias', views.verCategorias, name = 'ver_categorias'),
    path('myadmin/agregar-categorias', views.agregarCategorias, name = 'agregar_categorias'),
    path('myadmin/editar-categoria/<int:id>', views.editarCategoria, name = 'editar_categoria'),
    path('myadmin/eliminar-categoria/<int:id>', views.eliminarCategoria, name = 'eliminar_categoria'),
    
    path('sign_in', views.register, name='register'),
    path('user/', views.UsersList.as_view(), name = 'users_list'),
]