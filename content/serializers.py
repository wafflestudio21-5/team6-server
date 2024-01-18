from rest_framework import serializers
from .models import *


class PeopleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['peopleCD', 'name', 'photo']


class RoleSerializer(serializers.ModelSerializer):
    actor = PeopleInfoSerializer(read_only=True)

    class Meta:
        model = Role
        fields = ['actor', 'role', 'priority']


class ShowGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre']


class MovieSerializer(serializers.ModelSerializer):
    directors = PeopleInfoSerializer(many=True)
    writers = PeopleInfoSerializer(many=True)
    castings = RoleSerializer(many=True)
    genres = ShowGenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('plot', 'runtime', 'screening')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'