from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin, name='admin'),
    path('user/', views.user, name='user'),
    path('show_user/', views.show_user, name='show_user'),
    path('show_users/', views.show_users, name='show_users'),
    path('vote/', views.vote, name='vote'),
    path('user_login/', views.user_login, name='user_login'),
    path('detect_face/', views.detect_face, name='detect_face'),
    path('add_user/', views.add, name='add'),
    path('add_user_details/', views.add_user_details, name='add_user_details'),
    path('show_voter_details/', views.show_voter_details, name='show_voter_details'),
]
