from django.urls import path
from main.views.admin import pages, tags, stories, recommenders
from main.views.admin import users_management as um
from main.views.user import flashcard_collection, flashcards, user_apis, exercise_apis
from main.views import views, auth_views

# para cargar imagenes
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    # General views
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('stories/', views.storiesGallery, name="stories"),
    
    # Stories for admin
    path('myadmin/stories', stories.index, name = 'admin_stories'),
    path('myadmin/add-story/', stories.create, name = 'add_story'),
    path('myadmin/edit-story/<int:story_id>', stories.update, name = 'edit_story'),
    path('myadmin/del-story/<int:story_id>', stories.delete, name = 'delete_story'),

    # Tags
    path('myadmin/tags', tags.index, name = 'tags'),
    path('myadmin/add-tag', tags.create, name = 'add_tag'),
    path('myadmin/edit-tag/<int:tag_id>', tags.update, name = 'edit_tag'),
    path('myadmin/del-tag/<int:tag_id>', tags.delete, name = 'del_tag'),

    # Pages
    path('myadmin/view-pages/<slug:route>/', pages.index, name='view_pages'),
    path('myadmin/add-page/<slug:route>/<int:page_type>/', pages.create, name='add_page'),
    path('myadmin/edit-page/<slug:route>/<int:page_type>/<int:page_id>/', pages.update, name='edit_page'),
    path('myadmin/del-page/<int:id>/', pages.delete, name='del_page'),

    # Recommenders
    path('myadmin/recommenders/', recommenders.index, name="recommenders"),
    path('myadmin/recommenders/content-based-recommender/update', recommenders.updateCBRecommender, name="update_cb_recommender"),
    path('myadmin/recommenders/user-based-recommender/update', recommenders.updateUBRecommender, name="update_ub_recommender"),

    path('myadmin/recommenders/content-based-recommender/settings', recommenders.cbrUpdateSettings, name="cbr_settings"),
    path('myadmin/recommenders/user-based-recommender/settings', recommenders.ubrUpdateSettings, name="ubr_settings"),

    # Users management
    path('myadmin/users_management/', um.index, name='management_users'),
    path('myadmin/users_management/del/<int:user_id>/', um.delete, name='management_del_user'),
    path('myadmin/users_management/edit/<int:user_id>/', um.update, name='management_edit_user'),
    
    # Show stories content
    path('story/<slug:route>/', views.storyInfo, name = 'story_info'),
    path('story/<slug:route>/<int:page_number>/', views.pageDisplayer, name='story_content'),

    # Flashcards collections
    path('flashcards/', flashcard_collection.index, name='flashcards_collections'),
    path('flashcards/collection/add/', flashcard_collection.create, name='add_flashcards_collection'),
    path('flashcards/collection/del/<int:fc_collection_id>/', flashcard_collection.delete, name='del_flashcards_collection'),
    path('flashcards/collection/edit/<int:fc_collection_id>/', flashcard_collection.update, name='edit_flashcards_collection'),

    # Flashcards
    path('flashcards/<int:fc_collection_id>/', flashcards.index, name='flashcards'),
    path('flashcards/<int:fc_collection_id>/add/', flashcards.create, name='add_flashcard'),
    path('flashcards/del/<int:flashcard_id>/', flashcards.delete, name='del_flashcard'),
    path('flashcards/edit/<int:flashcard_id>/', flashcards.update, name='edit_flashcard'),

    # Another functions
    path('api/user/like-story/<int:story_id>', user_apis.likeStory, name = 'like_story'),
    path('api/user/save-story/<int:story_id>', user_apis.saveStory, name = 'save_story'),
    path('api/user/delete-answers/<int:story_id>', user_apis.deleteAnswers, name = 'delete_answers'),

    
    path('api/exercise/request_answer/', exercise_apis.request_answer, name="request_exercise_answer"),

    path('register', auth_views.register, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)