from django.urls import path
from .views import *

urlpatterns = [
    path('', CommentListCreateAPI.as_view()),
    path('<int:pk>', CommentRetrieveUpdateDestroyAPI.as_view()),
]