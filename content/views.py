from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from .serializers import *
from .paginations import *
from comment.permissions import IsOwnerOrReadOnly

from decimal import Decimal


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


class RatingAPI(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication,]

    def get_queryset(self, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        return Rating.objects.filter(movie=movie)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['rate'] = Decimal(request.data['rate'])
        request.data._mutable = False
        print(request.data)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print(self.request.user, self.kwargs['pk'])
        serializer.save(
            created_by=self.request.user,
            movie=Movie.objects.get(pk=self.kwargs['pk'])
        )


class RatingRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsOwnerOrReadOnly,]


class CarouselRetrieveAPI(generics.RetrieveAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer

