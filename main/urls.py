from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    #path('login', views.login, name='login'),
    
    path('sign_in', views.sign_in, name='sign_in'),
    path('user/', views.UsersList.as_view(), name = 'users_list'),
]