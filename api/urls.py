from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/', include('user.urls')),
    path('import-users/', include('user.urls')),
    path('rerun-process/', include('preprocess.urls')),
    path('match/<int:userid>/', views.user_match, name='match'),
    path('test/', views.test_cosine_similarity),
    path('predict/<uuid:matcher>/', views.predict, name='predict_match_full'),
    path('predict_one_on_one/<uuid:matcher>/<uuid:matchee>', views.predict_one_on_one, name='predict_match'),
]