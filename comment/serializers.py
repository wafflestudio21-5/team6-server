from rest_framework import serializers

from .models import *
from content.models import Rating
from waffleAuth.models import WaffleUser


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaffleUser
        fields = ['id', 'nickname', 'profile_photo']


class CommentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate']


class CommentSerializer(serializers.ModelSerializer):
    created_by = WriterSerializer(read_only=True)
    rating = CommentRatingSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'required': False, 'allow_null': True},
            'movie': {'required': False, 'allow_null': True},
        }

    def get_like_count(self, obj):
        return obj.likes.all().count()

    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            if obj.likes.filter(created_by=request.user).exists():
                return True
        return False

    def get_reply_count(self,obj):
        return obj.replies.all().count()


class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'movie']


class ReplySerializer(serializers.ModelSerializer):
    created_by = WriterSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    comment = ReplyCommentSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.likes.all().count()

    def get_liked_by_user(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            if obj.likes.filter(created_by=request.user).exists():
                return True
        return False
