from django.urls import path
from .views import *

urlpatterns = [
    path('', CommentListCreateAPI.as_view()),
    path('<int:pk>', CommentRetrieveUpdateDestroyAPI.as_view()),
    path('<int:object_id>/like', ProcessCommentLikeAPI.as_view()),
    path('<int:comment_id>/replies/', ReplyListCreateAPI.as_view()),
    path('replies/<int:reply_id>', ReplyRetrieveUpdateDestroyAPI.as_view()),
    path('replies/<int:object_id>/like', ProcessReplyLikeAPI.as_view()),
]