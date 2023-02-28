from django.urls import path
from main.views.admin import pages, tags, stories
from main.views.user import story_render, user_apis, exercise_apis
from main.views import views, auth_views as v

# para cargar imagenes
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    # General views
    path('', views.index, name='index'),
    path('saved/', views.savedStories, name='saved_stories'),
    path('liked/', views.likedStories, name='liked_stories'),

    # Stories
    path('myadmin/', stories.index, name = 'index_admin'),
    path('myadmin/add-story/', stories.create, name = 'add_story'),
    path('myadmin/edit-story/<int:story_id>', stories.update, name = 'edit_story'),
    path('myadmin/del-story/<int:story_id>', stories.delete, name = 'delete_story'),

    # Tags
    path('myadmin/add-tag', tags.create, name = 'add_tag'),
    path('myadmin/edit-tag/<int:tag_id>', tags.update, name = 'edit_tag'),
    path('myadmin/del-tag/<int:tag_id>', tags.delete, name = 'delete_tag'),

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
    
    path('api/exercise/request_answer/', exercise_apis.request_answer, name="request_exercise_answer"),

    path('api/filter_story/', user_apis.filterStories, name="filter_stories"),

    path('register', v.register, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)