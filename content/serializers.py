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
        fields = ['actor', 'role']


class MovieSerializer(serializers.ModelSerializer):
    directors = PeopleInfoSerializer(many=True)
    writers = PeopleInfoSerializer(many=True)
    castings = RoleSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('plot', 'runtime', 'screening')
