from rest_framework.pagination import CursorPagination as BaseCursorPagination


class MovieCursorPagination(BaseCursorPagination):
    page_size = 5


class CommentCursorPagination(BaseCursorPagination):
    page_size = 8