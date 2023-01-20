from django.urls import path
from . import vistas as v
from main.controllers.admin import pages, tags, stories
from main.controllers.user import story_render

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
    path('myadmin/add-page/<slug:route>/<int:page_type>', pages.create, name='add_page'),
    path('myadmin/edit-page/<slug:route>/<int:page_type>/<int:page_id>', pages.update, name='edit_page'),
    path('myadmin/del-page/<int:id>', pages.delete, name='del_page'),

    # for stories and related
    path('story/<slug:route>/', story_render.storyInfo, name = 'story_info'),
    path('story/<slug:route>/<int:page_number>/', story_render.storyContent, name='story_content'),

    # Todas las categorías y sus funciones
    path('myadmin/ver-categorias', tags.index, name = 'ver_categorias'),
    path('myadmin/agregar-categorias', tags.create, name = 'agregar_categorias'),
    path('myadmin/editar-categoria/<int:id>', tags.update, name = 'editar_categoria'),
    path('myadmin/eliminar-categoria/<int:id>', tags.delete, name = 'eliminar_categoria'),
    
    path('register', v.register, name='register'),
    path('user/', v.UsersList.as_view(), name = 'users_list'),

    path('test/', v.test, name='test'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)