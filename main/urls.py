from django.urls import path
from . import vistas as v
from main.controllers.admin import pages, tags, stories
from main.controllers.user import story_render, user_apis

# para cargar imagenes
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', v.index, name='index'),

    # Stories
    path('myadmin/', stories.index, name = 'index_admin'),
    path('myadmin/add-story/', stories.create, name = 'add_story'),
    path('myadmin/edit-story/<int:story_id>', stories.edit, name = 'edit_story'),
    path('myadmin/del-story/<int:story_id>', stories.delete, name = 'delete_story'),

    # Tags
    path('myadmin/ver-categorias', tags.index, name = 'ver_categorias'),
    path('myadmin/agregar-categorias', tags.create, name = 'agregar_categorias'),
    path('myadmin/editar-categoria/<int:id>', tags.update, name = 'editar_categoria'),
    path('myadmin/eliminar-categoria/<int:id>', tags.delete, name = 'eliminar_categoria'),

    # Pages
    path('myadmin/view-pages/<slug:route>/', pages.index, name='view_pages'),
    path('myadmin/add-page/<slug:route>/<int:page_type>/', pages.create, name='add_page'),
    path('myadmin/edit-page/<slug:route>/<int:page_type>/<int:page_id>/', pages.update, name='edit_page'),
    path('myadmin/del-page/<int:id>/', pages.delete, name='del_page'),

    # Show stories content
    path('story/<slug:route>/', story_render.storyInfo, name = 'story_info'),
    path('story/<slug:route>/<int:page_number>/', story_render.storyContent, name='story_content'),

    # Another functions
    path('api/user/like-story/<int:story_id>', user_apis.likeStory, name = 'like_story'),
    path('api/user/save-story/<int:story_id>', user_apis.saveStory, name = 'save_story'),
    
    path('register', v.register, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)