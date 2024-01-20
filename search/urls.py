from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *

urlpatterns = [
    path('users/<string:keyword>/',  UserSearchListView.as_view(), name='user-search'),
    path('movies/<string:keyword>/', MovieSearchListView.as_view(), name='movie-search'),
    path('<string:keyword>/', KeywordSearchListView.as_view(), name='keyword-search'),
]
