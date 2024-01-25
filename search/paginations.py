from rest_framework.pagination import PageNumberPagination


class MovieSearchPagination(PageNumberPagination):
    page_size = 9
    page_query_param = 'page'
    page_size_query_param = 'page_size'


class UserSearchPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    page_size_query_param = 'page_size'


class SearchPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
