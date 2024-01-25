from django.http import QueryDict
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError

from .models import *
from .serializers import *
from .paginations import *
from comment.permissions import IsOwnerOrReadOnly
from .permissions import IsOwner

from decimal import Decimal


class MovieListAPI(generics.ListAPIView):
    serializer_class = MovieListSerializer
    authentication_classes = [JWTAuthentication, ]

    def get_queryset(self, *args, **kwargs):
        if self.request.query_params.get('order'):
            order_options = {
                'latest': '-release_date',
                'box-office': '-cumulative_audience'
            }
            return Movie.objects.order_by(order_options[self.request.query_params.get('order')])[:30]
        return Movie.objects.order_by('-release_date')[:30]


class MovieRetrieveAPI(generics.RetrieveAPIView):
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [JWTAuthentication, ]


class RatingAPI(generics.ListCreateAPIView):
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication,]

    def get_queryset(self, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        return Rating.objects.filter(movie=movie)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['rate'] = Decimal(str(request.data['rate']))
        if isinstance(request.data, QueryDict):
            request.data._mutable = False
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])

        # 이미 유저가 영화에 대해 남긴 별점이 있는지 확인
        existing_rating = Rating.objects.filter(movie=movie, created_by=self.request.user).first()

        if existing_rating:
            raise ValidationError("You have already rated this movie.")
        else:
            # If no rating exists, create a new one
            serializer.save(
                created_by=self.request.user,
                movie=movie
            )

            # connect Rating to Comment if exists
            if Comment.objects.filter(movie=movie, created_by=self.request.user).exists():
                user_comment = Comment.objects.get(movie=movie, created_by=self.request.user)
                current_rating = Rating.objects.get(movie=movie, created_by=self.request.user)
                user_comment.rating = current_rating
                user_comment.save()


class RatingRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsOwnerOrReadOnly,]


class CarouselRetrieveAPI(generics.RetrieveAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer
    authentication_classes = [JWTAuthentication, ]


class StateCreateAPI(generics.CreateAPIView):
    serializer_class = StateSerializer
    queryset = State.objects.all()
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])

        # 이미 유저가 영화에 대해 상태를 설정한 적이 있는지 확인
        existing_rating = State.objects.filter(movie=movie, user=self.request.user).first()

        if existing_rating:
            raise ValidationError("You have already set state for this movie.")

        serializer.save(
            user=self.request.user,
            movie=movie
        )


class StateUpdateAPI(generics.UpdateAPIView):
    serializer_class = StateSerializer
    queryset = State.objects.all()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsOwner, ]
