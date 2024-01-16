from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests, json

from .serializers import MovieListSerializer, MovieDetailSerializer

KOBIS_API_KEY = settings.KOBIS_API_KEY
KMDB_API_KEY = settings.KMDB_API_KEY


@api_view(['GET'])
def kobis_movies_list(request):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
    params = {
        'key': KOBIS_API_KEY,
        'curPage': "1",
        'itemPerPage': "30",
        'movieNm': "기생충",
    }
    response = requests.get(url, params=params)
    movies_data = response.json()['movieListResult']['movieList']
    movie_serializer = MovieListSerializer(movies_data, many=True)

    # return Response(movies_data)
    return Response(movie_serializer.data)


@api_view(['GET'])
def kobis_movies_detail(request, pk):
    kobis_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    kobis_params = {
        'key': KOBIS_API_KEY,
        'movieCd': pk,
    }
    kobis_response = requests.get(kobis_url, params=kobis_params)
    movie_data = kobis_response.json()['movieInfoResult']['movieInfo']
    movie_title = movie_data['movieNm']
    movie_director = movie_data['directors'][0]['peopleNm']

    kmdb_url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2'
    kmdb_params = {
        'ServiceKey': KMDB_API_KEY,
        'listCount': "1",
        'title': movie_title,
        'director': movie_director,
    }
    kmdb_response = requests.get(kmdb_url, params=kmdb_params)
    kmdb_data = kmdb_response.json()['Data'][0]['Result'][0]
    kmdb_poster = kmdb_data['posters'].split('|')[0]
    kmdb_plot = kmdb_data['plots']['plot'][0]['plotText']

    # Add kmdb_poster and kmdb_plot to movie_data
    movie_data['poster'] = kmdb_poster
    movie_data['plot'] = kmdb_plot

    movie_serializer = MovieDetailSerializer(movie_data)

    return Response(movie_serializer.data)


@api_view(['GET'])
def kobis_box_office(request):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    params = {
        'key' : KOBIS_API_KEY,
        'targetDt' : '20240114', # 추후 현재 Date로 바꿔야 할 것
    }
    response = requests.get(url, params=params)
    movies_data = response.json()['boxOfficeResult']['dailyBoxOfficeList']

    return Response(movies_data)



@api_view(['GET'])
def kmdb_movies(request):
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2'
    params = {
        'ServiceKey': KMDB_API_KEY,
        'listCount': "1",
        'title': '광해, 왕이 된 남자',
        'director': '추창민',
    }
    response = requests.get(url, params=params)
    movies_data = response.json()['Data']
    movie_serializer = MovieListSerializer(movies_data, many=True)

    # return Response(movie_serializer.data)
    return Response(movies_data)