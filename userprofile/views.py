from django.shortcuts import render
from waffleAuth.models import WaffleUser
from content.models import Movie, Rating, State
from comment.models import Comment, Like
# Create your views here.
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import StateSerializer, UserRatingSerializer, CommentSerializer, UserDetailSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class UserDetailView(RetrieveAPIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    queryset = WaffleUser.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'pk'


class UserFollowView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user_to_follow = WaffleUser.objects.get(pk=pk)
            if request.user == user_to_follow:
                return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            request.user.following.add(user_to_follow)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except WaffleUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
