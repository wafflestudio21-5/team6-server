from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *


urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='user-followers'),
    path('<int:user_id>/followings/', FollowingsListView.as_view(), name='user-following'),
    path('<int:pk>/comments/', UserCommentsListView.as_view(), name='user-comments'),
    path('<int:user_id>/ratings/', UserRatingListView.as_view(), name='user-ratings'),
    ]