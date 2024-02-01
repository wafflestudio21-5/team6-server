from django.shortcuts import render
from django.db.models import Q

from waffleAuth.models import WaffleUser
from content.models import Movie
from .serializers import *
from .paginations import *

from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class SearchListAPIView(ListAPIView):
    #pagination_class = SearchPagination
    authentication_classes = [JWTAuthentication]

    def get_pagination_class(self):
        category = self.request.query_params.get('category', 'movie')
        if category == 'users':
            return UserSearchPagination
        else:
            return MovieSearchPagination

    pagination_class = property(get_pagination_class)

    def get_serializer_class(self):
        category = self.request.query_params.get('category', 'movie')
        if category == 'users':
            return UserListSerializer
        else:
            return MovieListSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', 'movie')
        query = self.request.query_params.get('query', '')

        if category == 'users':
            if query:
                queryset = WaffleUser.objects.filter(nickname__icontains=query)
            else:
                queryset = WaffleUser.objects.none()
        else:
            if query:
                queryset = Movie.objects.filter(Q(title_ko__icontains=query) | Q(title_original__icontains=query))
            else:
                queryset = Movie.objects.none()

        return queryset


class KeywordSearchListAPIView(ListAPIView):
    serializer_class = MovieTitleListSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            movie_titles = Movie.objects.filter(title_ko__icontains=query)
        else:
            movie_titles = None
        return movie_titles
