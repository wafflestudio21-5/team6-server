from django.urls import path
from . import views


urlpatterns = [
    path("movies/kobis/", views.kobis_movies),
    path("movies/kmdb/", views.kmdb_movies),
]
