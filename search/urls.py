from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *

urlpatterns = [
    path('',  SearchListAPIView.as_view(), name='search'), #query로 받도록
    path('keyword/', KeywordSearchListAPIView.as_view(), name='keyword-search'),
]
