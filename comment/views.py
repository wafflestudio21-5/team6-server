from rest_framework.generics import get_object_or_404
from rest_framework import generics
from django.db.models import Count, F

from .serializers import *
from .paginations import *
from .models import *


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentCursorPagination

    def get_queryset(self, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        order_options = {
            'like': '-like_count',
            'high-rating': '-rate_count',
            'low-rating': 'rate_count',
            'created': '-created_at'
        }
        if self.request.query_params.get('order'):
            self.pagination_class.ordering = order_options[self.request.query_params.get('order')]
            if 'rate' in order_options[self.request.query_params.get('order')]:
                return Comment.objects.filter(movie=movie).exclude(rating__isnull=True).annotate(like_count=Count('likes'), rate_count=F('rating__rate'))
        return Comment.objects.filter(movie=movie).annotate(like_count=Count('likes'), rate_count=F('rating__rate'))

    def get(self, request, *args, **kwargs):
        comments = self.get_queryset()
        for comment in comments:
            comment.like_count = Like.objects.filter(comment__id=comment.id).count()
            comment.save()
        return super().get(request, *args, **kwargs)
