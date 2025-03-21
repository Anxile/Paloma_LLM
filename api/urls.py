from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('todo/', views.todo, name='todo'),
]