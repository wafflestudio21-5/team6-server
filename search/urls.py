from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *

urlpatterns = [
    path('users/',  UserSearchListAPIView.as_view(), name='user-search'), #query로 받도록
    path('movies/', MovieSearchListAPIView.as_view(), name='movie-search'),
    path('keyword/', KeywordSearchListAPIView.as_view(), name='keyword-search'),
]
