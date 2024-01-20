from django.shortcuts import render

from waffleAuth.models import WaffleUser
from content.models import Movie

from rest_framework.generics import ListAPIView


# query로 받도록

class UserSearchListAPIView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.following.all()


class MovieSearchListAPIView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.following.all()

class KeywordSearchListAPIView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.following.all()
