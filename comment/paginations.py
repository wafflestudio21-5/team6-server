from rest_framework.pagination import CursorPagination as BaseCursorPagination

from .models import Comment


class CommentCursorPagination(BaseCursorPagination):
    page_size = 8
    ordering = '-like_count'


class ReplyCursorPagination(BaseCursorPagination):
    page_size =8
    ordering = '-created_at'
