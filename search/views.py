from django.shortcuts import render

from waffleAuth.models import WaffleUser
from content.models import Movie

from rest_framework.generics import ListAPIView

class UserSearchListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.following.all()


class MovieSearchListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.following.all()

class KeywordSearchListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.following.all()
