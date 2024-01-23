from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from rest_framework.exceptions import ValidationError

from django.db.models import Count, F
from django.contrib.contenttypes.models import ContentType

from .serializers import *
from .paginations import *
from .models import *
from .permissions import IsOwnerOrReadOnly


class CommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentCursorPagination
    authentication_classes = [JWTAuthentication,]

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
                return Comment.objects.filter(movie=movie).exclude(rating__isnull=True).annotate(
                    like_count=Count('likes'), rate_count=F('rating__rate'))
        return Comment.objects.filter(movie=movie).annotate(like_count=Count('likes'), rate_count=F('rating__rate'))

    def get(self, request, *args, **kwargs):
        comments = self.get_queryset()
        for comment in comments:
            comment.like_count = Like.objects.filter(comment__id=comment.id).count()
            comment.save()
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))

        # 이미 유저가 영화에 대해 작성한 코멘트가 있는지 확인
        existing_comment = Comment.objects.filter(movie=movie, created_by=self.request.user).first()

        if existing_comment:
            raise ValidationError("You have already commented on this movie.")
        else:
            serializer.save(
                created_by=self.request.user,
                movie=movie
            )


class CommentRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsOwnerOrReadOnly,]


class ProcessCommentLikeAPI(APIView):
    def post(self, request, *args, **kwargs):
        like, created = Like.objects.get_or_create(
            created_by=self.request.user,
            object_id=self.kwargs.get('object_id'),
            content_type_id=ContentType.objects.get(model='comment').id,
        )
        if not created:
            like.delete()

        return Response({"message": "success"}, status=status.HTTP_200_OK,)


class ReplyListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ReplySerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsOwnerOrReadOnly, ]
    pagination_class = CursorPagination

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        queryset = Reply.objects.filter(comment_id=comment_id).order_by('updated_at')

        return queryset

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('comment_id'))
        serializer.save(
            created_by=self.request.user,
            comment=comment
        )


class ReplyRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsOwnerOrReadOnly,]
    lookup_url_kwarg = 'reply_id'


class ProcessReplyLikeAPI(APIView):
    def post(self, request, *args, **kwargs):
        like, created = Like.objects.get_or_create(
            created_by=self.request.user,
            object_id=self.kwargs.get('object_id'),
            content_type_id=ContentType.objects.get(model='reply').id,
        )
        if not created:
            like.delete()

        return Response({"message": "success"}, status=status.HTTP_200_OK,)
