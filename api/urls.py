from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('match/<int:userid>', views.user_match, name='match'),
    path('create/', views.create_user, name='create'),
]