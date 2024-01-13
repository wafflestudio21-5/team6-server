from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    movieCD = serializers.CharField(source='movieCd')
    openDt = serializers.DateField(allow_null=True)

    class Meta:
        model = Movie
        fields = '__all__'
