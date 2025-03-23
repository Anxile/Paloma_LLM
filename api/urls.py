from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_user, name='create'),
    path('match/<int:userid>/', views.user_match, name='match'),

]