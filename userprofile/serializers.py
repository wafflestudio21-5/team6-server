from rest_framework import serializers
from waffleAuth.models import WaffleUser
from content.models import Movie, Rating, State
from comment.models import Comment, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaffleUser
        fields = ['id', 'username', 'nickname', 'bio', 'profile_photo', 'background_photo']


class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = WaffleUser
        fields = ['id', 'username', 'nickname', 'bio', 'profile_photo', 'background_photo', 'followers_count', 'following_count']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'movie', 'content', 'rating', 'created_at', 'updated_at', 'likes']


# serializers.py
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'movieCD', 'title_ko', 'title_original', 'plot', 'runtime',
            'prod_country', 'poster', 'release_date', 'cumulative_audience',
            'screening'
        ]


class UserRatingSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'rating', 'movie', 'updated_at', 'created_by']
        depth = 1  # This will nest the movie information one level deep


class StateSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = State
        fields = ['id', 'movie', 'state']
