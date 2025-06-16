from django.urls import path,include
from . import views

urlpatterns = [
    path('user/', include('user.urls')),
    path('rerun-process/', include('pre_process.urls')),
    path('experiment/', include('experiment.urls')),
    path('match/', include('match_making.urls')),
    
    # path('match/<int:userid>/', views.user_match, name='match'),
    # path('test/', views.test_cosine_similarity),
    # path('predict/<uuid:matcher>/', views.predict, name='predict_match_full'),
    # path('predict_one_on_one/<uuid:matcher>/<uuid:matchee>', views.predict_one_on_one, name='predict_match'),
]