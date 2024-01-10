from django.shortcuts import render
from waffleAuth.models import WaffleUser
from .models import Comment, Like, Rating, State
# Create your views here.
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import StateSerializer, UserRatingSerializer, CommentSerializer, FollowerSerializer, FollowingSerializer, UserDetailSerializer, UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = WaffleUser.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'pk'


class FollowersListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.followers.all()


class FollowingsListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.following.all()


class UserCommentsListView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Comment.objects.filter(created_by_id=user_id)


# views.py
class UserRatingListView(ListAPIView):
    serializer_class = UserRatingSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        # Use `select_related` for better performance, as it will join the related Movie table
        return Rating.objects.filter(created_by_id=user_id).select_related('movie')


class UserMovieStateListView(ListAPIView):
    serializer_class = StateSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        state = self.kwargs.get("state")
        return State.objects.filter(user_id=user_id, state=state)

