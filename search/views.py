from django.shortcuts import render
from django.db.models import Q

from waffleAuth.models import WaffleUser
from content.models import Movie
from .serializers import *

from rest_framework.generics import ListAPIView


# query로 받도록

class SearchListAPIView(ListAPIView):

    def get_serializer_class(self):
        category = self.request.query_params.get('category', 'movie')
        if category in ['users']:
            serializer_class = UserListSerializer
        else:
            serializer_class = MovieListSerializer
        return serializer_class

    def get_queryset(self):
        category = self.request.query_params.get('category', 'movie')
        query = self.request.query_params.get('query', '')

        if category in ['users']:
            if query:
                query_lists = WaffleUser.objects.filter(username__icontains=query)
            else:
                query_lists = WaffleUser.objects.all()  #왓챠피디아에서는 키워드 없으면 검색 불가
        else:
            if query:
                query_lists = Movie.objects.filter(Q(title_ko__icontains=query) | Q(title_original__icontains=query))
            else:
                query_lists = Movie.objects.all() #왓챠피디아에서는 키워드 없으면 검색 불가
        return query_lists


class KeywordSearchListAPIView(ListAPIView):
    serializer_class = MovieTitleListSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if query:
            movie_titles = Movie.objects.filter(title_ko__icontains=query)
        else:
            movie_titles = None
        return movie_titles
