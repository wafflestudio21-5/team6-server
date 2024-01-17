from rest_framework import serializers
from .models import Movie as TransmitMovie
from content.models import Movie


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




