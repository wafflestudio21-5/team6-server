from rest_framework import generics

from .models import *
from .serializers import *
from .paginations import *


class MovieListAPI(generics.ListAPIView):
    serializer_class = MovieListSerializer
    pagination_class = MovieCursorPagination

    def get_queryset(self, *args, **kwargs):
        order_options = {
            'latest': 'release_date',
            'boxoffice': 'cumulative_audience'
        }
        queryset = Movie.objects.order_by(order_options[kwargs['order']])
        return super().get_queryset()


class MovieRetrieveAPI(generics.RetrieveAPIView):
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
