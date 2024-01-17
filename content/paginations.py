from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination


class MoviePageNumberPagination(BasePageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page_size'
