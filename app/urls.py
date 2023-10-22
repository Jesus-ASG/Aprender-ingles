from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from main.views.auth_views import Login, Logout
from main.views.views import test_not_found

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/redirect/', include(('main.urls', 'main'))),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('api_generate_token/', views.obtain_auth_token),
    path('404/', test_not_found),
]

urlpatterns += staticfiles_urlpatterns()

handler404 = 'main.views.views.not_found_page'