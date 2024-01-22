from rest_framework.pagination import PageNumberPagination


class RatingPagination(PageNumberPagination):
    page_size = 15
