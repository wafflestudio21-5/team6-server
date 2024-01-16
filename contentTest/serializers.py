from rest_framework import serializers
from .models import Movie


class MovieListSerializer(serializers.ModelSerializer):
    poster = serializers.URLField()

    class Meta:
        model = Movie
        fields = ['movieCd', 'movieNm', 'nationAlt', 'openDt', 'poster']


class MovieDetailSerializer(serializers.ModelSerializer):
    poster = serializers.URLField()
    plot = serializers.CharField()

    class Meta:
        model = Movie
        fields = '__all__'




