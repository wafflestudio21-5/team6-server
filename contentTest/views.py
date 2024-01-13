from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests, json

from .serializers import MovieSerializer

KOBIS_API_KEY = settings.KOBIS_API_KEY
KMDB_API_KEY = settings.KMDB_API_KEY


@api_view(['GET'])
def movies(request):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
    params = {
        'key': KOBIS_API_KEY,
        'curPage': "1",
        'itemPerPage': "20",
    }
    response = requests.get(url, params=params)
    movies_data = response.json()['movieListResult']
    movie_serializer = MovieSerializer(movies_data, many=True)

    # return Response(movie_serializer.data)
    return Response(movies_data)
