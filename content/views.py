from rest_framework import generics

from .models import *
from .serializers import *
from .paginations import *


class MovieListAPI(generics.ListAPIView):
    serializer_class = MovieListSerializer
    pagination_class = MoviePageNumberPagination

    def get_queryset(self, *args, **kwargs):
        order_options = {
            'latest': '-release_date',
            'box-office': '-cumulative_audience'
        }
        return Movie.objects.order_by(order_options[self.request.query_params.get('order')])[:20]


class MovieRetrieveAPI(generics.RetrieveAPIView):
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
