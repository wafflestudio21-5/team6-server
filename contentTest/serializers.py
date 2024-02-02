from rest_framework import serializers
from .models import TransmitMovie as TransmitMovie
from content.models import Movie, BoxOffice, BoxOfficeMovie, Rating
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
    my_rate = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()

    class Meta:
        model = BoxOfficeMovie
        fields = ['movie', 'movie_id', 'my_rate', 'rank', 'average_rate']

    def get_my_rate(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Use obj.movie to refer to the associated Movie instance
            if Rating.objects.filter(movie=obj.movie, created_by=request.user).exists():
                my_rating = Rating.objects.get(movie=obj.movie, created_by=request.user)
                return my_rating.rate
        return None

    def get_average_rate(self, obj):
        if Rating.objects.filter(movie=obj).exists():
            return round(
                sum(map(lambda x: x.rate, Rating.objects.filter(movie=obj))) / len(Rating.objects.filter(movie=obj)), 1)
        return None


class BoxOfficeSerializer(serializers.ModelSerializer):
    movies = BoxOfficeMovieSerializer(source='boxofficemovie_set', many=True)

    class Meta:
        model = BoxOffice
        fields = ('id', 'date', 'movies')
        depth = 1
