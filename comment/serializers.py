from rest_framework import serializers

from .models import *
from content.models import Rating
from waffleAuth.models import WaffleUser


class CommentWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaffleUser
        fields = ['id', 'nickname', 'profile_photo']


class CommentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate']


class CommentSerializer(serializers.ModelSerializer):
    created_by = CommentWriterSerializer(read_only=True)
    rating = CommentRatingSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'has_spoiler', 'created_at', 'updated_at', 'movie', 'rating']
