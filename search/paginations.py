from rest_framework.pagination import PageNumberPagination

class SearchPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page_size'
