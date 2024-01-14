from django.urls import path
from .views import *

urlpatterns = [
    path('<str:pk>', CommentListAPIView.as_view()),
]