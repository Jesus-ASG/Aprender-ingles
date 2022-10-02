from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('myadmin', views.IndexAdmin.as_view(), name='index_admin'),
    path('myadmin/agregar-historias', views.agregarHistorias, name = 'agregar_historias'),
    #path('login', views.login, name='login'),
    
    path('sign_in', views.register, name='register'),
    path('user/', views.UsersList.as_view(), name = 'users_list'),
]