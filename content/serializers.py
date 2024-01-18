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
    average_rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_average_rate(self, obj):
        if Rating.objects.filter(movie=obj).exists():
            return round(sum(map(lambda x: x.rate, Rating.objects.filter(movie=obj)))/len(Rating.objects.filter(movie=obj)), 1)
        return None


class MovieListSerializer(serializers.ModelSerializer):
    average_rate = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        exclude = ('plot', 'runtime', 'screening')

    def get_average_rate(self, obj):
        if Rating.objects.filter(movie=obj).exists():
            return round(sum(map(lambda x: x.rate, Rating.objects.filter(movie=obj)))/len(Rating.objects.filter(movie=obj)), 1)
        return None


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'