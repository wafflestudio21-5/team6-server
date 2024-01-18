from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
import requests, json

from .tools import *
from .serializers import MovieListSerializer, MovieDetailSerializer, MovieImportSerializer
from content.models import Movie, People, Role, Genre

from datetime import datetime

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
    return Response(movies_data, status=status.HTTP_200_OK)
    # movie_serializer = MovieListSerializer(movies_data, many=True)

    # return Response(movies_data)
    # return Response(movie_serializer.data)


class KobisRawData(APIView):
    def get(self, request, pk):
        kobis_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        kobis_params = {
            'key': KOBIS_API_KEY,
            'movieCd': pk,
        }
        kobis_response = requests.get(kobis_url, params=kobis_params)
        movie_data = kobis_response.json()['movieInfoResult']['movieInfo']
        return Response(movie_data, status=status.HTTP_200_OK)


class KMBDRawData(APIView):
    def get(self, request, pk):
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

        return Response(kmdb_data)


class ImportMovie(generics.CreateAPIView):
    serializer_class = MovieImportSerializer
    queryset = Movie.objects.all()

    def create(self, request, *args, **kwargs):
        #get information from Kobis - title, runtime, prod_country, release_date
        moviePK = self.kwargs.get('pk')
        kobis_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        kobis_params = {
            'key': KOBIS_API_KEY,
            'movieCd': moviePK,
        }
        kobis_response = requests.get(kobis_url, params=kobis_params)
        movie_data = kobis_response.json()['movieInfoResult']['movieInfo']

        data = dict()

        data['movieCD'] = self.kwargs.get('pk')
        data['title_ko'] = movie_data['movieNm']
        if movie_data['movieNmOg']:
            data['title_original'] = movie_data['movieNmOg']
        else:
            if movie_data['nations'][0]['nationNm'] != '한국':
                data['title_original'] = movie_data['movieNmEn']
            else:
                data['title_original'] = movie_data['movieNm']
        data['runtime'] = int(movie_data['showTm'])
        data['prod_country'] = movie_data['nations'][0]['nationNm']
        data['release_date'] = datetime.strptime(movie_data['openDt'], '%Y%m%d').date()

        #get information from KMDB - plot, poster
        kmdb_url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2'
        kmdb_params = {
            'ServiceKey': KMDB_API_KEY,
            'listCount': "1",
            'title': data['title_ko'],
            'director': movie_data['directors'][0]['peopleNm']
        }
        kmdb_response = requests.get(kmdb_url, params=kmdb_params)
        kmdb_data = kmdb_response.json()['Data'][0]['Result'][0]
        data['plot'] = kmdb_data['plots']['plot'][0]['plotText']
        data['poster'] = kmdb_data['posters'].split('|')[0]

        #create model
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        created_movie = Movie.objects.get(pk=data['movieCD'])

        #set genres
        genres = movie_data['genres']
        for genre_datum in genres:
            genre, _ = Genre.objects.get_or_create(genre=genre_datum['genreNm'])
            created_movie.genres.add(genre)

        #set directors
        directors_data = kmdb_data['directors']['director']
        directors_name = set()
        staffs_data = kmdb_data['staffs']['staff']
        for director_datum in directors_data:
            director, _ = People.objects.get_or_create(
                pk='d' + generate_director_code(director_datum['directorId']),
                name=generate_name(director_datum['directorNm'].split()).rstrip()
            )
            director.is_director = True
            directors_name.add(director.name)
            for staff_datum in staffs_data:
                if staff_datum['staffNm'] == director.name and staff_datum['staffRoleGroup'] == '각본':
                    director.is_writer = True
                    created_movie.writers.add(director)
            director.save()
            created_movie.directors.add(director)

        #set starring
        actors_data = kmdb_data['actors']['actor']
        priority = 0
        for actor_data in actors_data:
            if actor_data['actorId']:
                actor, _ = People.objects.get_or_create(
                    pk='a' + actor_data['actorId'],
                    name=actor_data['actorNm']
                )
                actor.is_actor = True
                actor.save()
                created_movie.casts.add(actor)
                for staff_datum in staffs_data:
                    if staff_datum['staffNm'] == actor.name:
                        Role.objects.create(
                            role=generate_role(staff_datum['staffRole']),
                            actor=actor,
                            priority=priority,
                            movie=created_movie
                        )
                priority += 1

        #set starring
        for staff_datum in staffs_data:
            if staff_datum['staffRoleGroup'] == '각본' and staff_datum['staffNm'] not in directors_name:
                if People.objects.filter(is_writer=True, name=staff_datum['staffNm']).exists():
                    writer = People.objects.get(is_writer=True, name=staff_datum['staffNm'])
                    created_movie.writers.add(writer)
                else:
                    writer = People.objects.create(
                        name=staff_datum['staffNm'],
                        is_writer=True,
                        pk='w' + generate_writer_code()
                    )
                    created_movie.writers.add(writer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET', 'POST'])
def kobis_movies_detail(request, pk):
    if request.method == 'GET':
        # KOBIS 로직. movieCD를 통해 Detail API에서 가져올 수 있는 것들 가져옴
        kobis_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        kobis_params = {
            'key': KOBIS_API_KEY,
            'movieCd': pk,
        }
        kobis_response = requests.get(kobis_url, params=kobis_params)
        movie_data = kobis_response.json()['movieInfoResult']['movieInfo']
        movie_title = movie_data['movieNm']
        movie_director = movie_data['directors'][0]['peopleNm']
        movie_nation = movie_data['nations'][0]['nationNm']

        # KMDB 로직. KOBIS에서 가져온 제목과 감독 이용해 검색하여, plot과 poster 가져옴
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
        movie_data['nationAlt'] = movie_nation

        movie_serializer = MovieDetailSerializer(movie_data)

        return Response(movie_serializer.data)

    elif request.method == 'POST':
        movie_serializer = MovieDetailSerializer(data=request.data)

        if movie_serializer.is_valid():
            # Save the data to the database
            movie_serializer.save()
            return Response(movie_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def kobis_box_office(request):
    # boxoffice list 불러오기
    boxoffice_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    boxoffice_params = {
        'key': KOBIS_API_KEY,
        'targetDt': '20240115',  # 추후 현재 Date로 바꿔야 할 것 -> 어차피 DB 주입한다면 그냥 상수로 해도 될 것 같다
    }
    response = requests.get(boxoffice_url, params=boxoffice_params)
    movies_data = response.json()
    return Response(movies_data)
'''
    for movie in movies_data:
        movie_title = movie['movieNm']
        kmdb_url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2'
        kmdb_params = {
            'ServiceKey': KMDB_API_KEY,
            'listCount': "1",
            'title': movie_title,
            # director를 불러오려면 KMDB_DETAIL을 써야 하기 때문에 여기에서 제외함. 어차피 DB 주입한다면 크게 신경 안 써도 될 것 같다.
        }
        kmdb_response = requests.get(kmdb_url, params=kmdb_params)
        kmdb_data = kmdb_response.json()['Data'][0]['Result'][0]
        kmdb_poster = kmdb_data['posters'].split('|')[0]

        movie['poster'] = kmdb_poster

    movie_serializer = MovieListSerializer(movies_data, many=True)
    return Response(movie_serializer.data)
'''


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


@api_view(['GET'])
def kobis_people(request, pk):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'
    params = {
        'key': KOBIS_API_KEY,
        'itemPerPage': "100",
        'filmoNames': pk,
    }
    response = requests.get(url, params=params)
    people_data = response.json()

    return Response(people_data)
