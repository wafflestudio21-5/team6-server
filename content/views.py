from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *
from .paginations import *


class MovieListAPI(generics.ListAPIView):
    serializer_class = MovieListSerializer
    pagination_class = MoviePageNumberPagination

    def get_queryset(self, *args, **kwargs):
        if self.request.query_params.get('order'):
            order_options = {
                'latest': '-release_date',
                'box-office': '-cumulative_audience'
            }
            return Movie.objects.order_by(order_options[self.request.query_params.get('order')])[:20]
        return Movie.objects.order_by('-release_date')[:20]


class MovieRetrieveAPI(generics.RetrieveAPIView):
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class RatingAPI(APIView):
    def get_object(self, pk):
        movie = generics.get_object_or_404(Movie, pk=pk)
        return movie

    def get(self, request, pk):
        movie = self.get_object(pk)
        ratings = round(sum(map(lambda x: x.rate,Rating.objects.filter(movie=movie)))/len(Rating.objects.filter(movie=movie)),1)
        data = {'movieCD': pk, 'rating': ratings}
        return Response(data, status=status.HTTP_200_OK)