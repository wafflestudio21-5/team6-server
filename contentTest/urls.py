from django.urls import path
from . import views


urlpatterns = [
    path('<str:pk>/kobis', views.KobisRawData.as_view()),
    path('<str:pk>/kmdb', views.KMBDRawData.as_view()),
    path('import/<str:pk>', views.ImportMovie.as_view()),
    path("movies/kobis/", views.kobis_movies_list),
    path("movies/<str:pk>", views.kobis_movies_detail),
    path("movies/boxoffice/", views.kobis_box_office),
    path("movies/kmdb/", views.kmdb_movies),
    path("people/<str:pk>", views.kobis_people),
]
