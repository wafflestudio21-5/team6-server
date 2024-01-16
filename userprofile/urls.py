from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *


urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='user-followers'),
    path('<int:user_id>/followings/', FollowingsListView.as_view(), name='user-following'),
    path('add/follow/', UserFollowView.as_view(), name='user-add-follow'),
    path('<int:pk>/comments/', UserCommentsListView.as_view(), name='user-comments'),
    path('<int:user_id>/ratings/', UserRatingListView.as_view(), name='user-ratings'),
    path('<int:user_id>/movies/watching/', UserMovieStateListView.as_view(), {'state': 'watching'}, name='user-watching-movies'),
    path('<int:user_id>/movies/want_to_watch/', UserMovieStateListView.as_view(), {'state': 'want_to_watch'}, name='user-want-to-watch-movies'),
    path('<int:user_id>/movies/not_interested/', UserMovieStateListView.as_view(), {'state': 'not_interested'}, name='user-not-interested-movies'),

    ]