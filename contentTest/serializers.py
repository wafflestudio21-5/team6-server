from rest_framework import serializers
from .models import TransmitMovie as TransmitMovie
from content.models import Movie, BoxOffice, BoxOfficeMovie
from content.serializers import MovieSerializer


class MovieImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate(self, attrs):
        fieldlist = [
            'title_ko',
            'title_original',
            'plot',
            'runtime',
            'prod_country',
            'poster',
            'release_date',
            'cumulative_audience',
            'screening'
        ]

        for single_field in fieldlist:
            if single_field in attrs:
                self.fields[single_field].required = False

        return attrs


class MovieListSerializer(serializers.ModelSerializer):
    poster = serializers.URLField()

    class Meta:
        model = TransmitMovie
        fields = ['movieCd', 'movieNm', 'nationAlt', 'openDt', 'poster']


class MovieDetailSerializer(serializers.ModelSerializer):
    poster = serializers.URLField()
    plot = serializers.CharField()
    nationAlt = serializers.CharField()

    class Meta:
        model = TransmitMovie
        fields = '__all__'



class MovieImport2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class BoxOfficeMovieSerializer(serializers.ModelSerializer):
    movie = MovieImport2Serializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True
    )

    class Meta:
        model = BoxOfficeMovie
        fields = ['movie', 'movie_id', 'rank']

class BoxOfficeSerializer(serializers.ModelSerializer):
    movies = BoxOfficeMovieSerializer(source='boxofficemovie_set', many=True)

    class Meta:
        model = BoxOffice
        fields = ('id', 'date', 'movies')
        depth = 1
