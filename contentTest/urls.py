from django.urls import path
from . import views


urlpatterns = [
    path("movies/kobis/", views.kobis_movies_list),
    path("movies/<str:pk>", views.kobis_movies_detail),
    path("movies/boxoffice/", views.kobis_box_office),
    path("movies/kmdb/", views.kmdb_movies),
]
