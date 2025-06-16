from django.urls import path
from . import views


urlpatterns = [
    path('<int:userid>/', views.match_making),
]