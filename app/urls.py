from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from main.vistas import Login, Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/redirect/', include(('main.urls', 'main'))),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('api_generate_token/', views.obtain_auth_token),
]
