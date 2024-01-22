from django.urls import path
from .views import *

urlpatterns = [
    path('', CommentListCreateAPI.as_view()),
    path('<int:pk>', CommentRetrieveUpdateDestroyAPI.as_view()),
    path('<int:object_id>/like', ProcessCommentLikeAPI.as_view()),
    path('<int:comment_id>/replies/', ReplyListAPI.as_view()),
]