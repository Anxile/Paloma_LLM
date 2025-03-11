from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_form, name='submit_form'),
    path('match_result/', views.match_result, name='match_result'),
]