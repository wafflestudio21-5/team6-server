from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>', CommentListAPIView.as_view()),
]