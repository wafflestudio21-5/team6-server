from rest_framework.generics import get_object_or_404
from rest_framework import generics

from .serializers import *
from .paginations import *
from .models import *


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentCursorPagination

    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(movie=movie)

    def get(self, request, *args, **kwargs):
        comments = self.get_queryset()
        for comment in comments:
            comment.like_count = Like.objects.filter(comment__id=comment.id).count()
            comment.save()
        return super().get(request, *args, **kwargs)
