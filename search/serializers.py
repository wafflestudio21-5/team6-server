from rest_framework import serializers
from content.models import Movie, People
from comment.models import Comment, Rating
from waffleAuth.models import WaffleUser
from django.db.models import Count, F


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['peopleCD', 'name']


class MovieTitleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'movieCD', 'title_ko',
        ]


class MovieListSerializer(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'movieCD', 'title_ko',
            'prod_country', 'poster', 'release_date',
            'directors',
        ]

    def get_directors(self, obj):
        # Filtering to get only directors of the movie
        directors = obj.directors.all()
        return DirectorSerializer(directors, many=True).data


class UserListSerializer(serializers.ModelSerializer):
    rate_num = serializers.SerializerMethodField()
    comment_num = serializers.SerializerMethodField()
    class Meta:
        model = WaffleUser
        fields =[
            'id', 'username', 'nickname', 'profile_photo', 'rate_num', 'comment_num'
        ]


    def get_rate_num(self, obj):
        return Rating.objects.filter(created_by__id=obj.id).count()

    def get_comment_num(self, obj):
        return Comment.objects.filter(created_by__id=obj.id).count()
