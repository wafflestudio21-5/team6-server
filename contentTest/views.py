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
def kobis_movies(request):
    # url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    params = {
        'key': KOBIS_API_KEY,
        'targetDt': '20240114',
        # 'curPage': "1",
        # 'itemPerPage': "30",
    }
    response = requests.get(url, params=params)
    # movies_data = response.json()['movieListResult']['movieList']
    movies_data = response.json()
    movie_serializer = MovieSerializer(movies_data, many=True)

    # return Response(movie_serializer.data)
    return Response(movies_data)


@api_view(['GET'])
def kmdb_movies(request):
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2'
    params = {
        'ServiceKey': KMDB_API_KEY,
        'listCount': "3",
    }
    response = requests.get(url, params=params)
    movies_data = response.json()['Data']
    movie_serializer = MovieSerializer(movies_data, many=True)

    # return Response(movie_serializer.data)
    return Response(movies_data)