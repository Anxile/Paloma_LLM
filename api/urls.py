from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_user, name='create'),
    path('match/<int:userid>/', views.user_match, name='match'),
    path('import-users/', views.import_user, name='import-users'),
    path('test/', views.test_cosine_similarity),
    path('predict/<uuid:matcher>/', views.predict, name='predict_match_full'),
    path('predict_one_on_one/<uuid:matcher>/<uuid:matchee>', views.predict_one_on_one, name='predict_match'),
]