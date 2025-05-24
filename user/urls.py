from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='user_index'),
    path('create/', views.create_user, name='user_create'),
    path('import/', views.import_user, name='user_import'),
]