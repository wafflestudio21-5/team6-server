from rest_framework import serializers
from .models import *
from comment.models import Comment
from comment.serializers import CommentSerializer
from .validators import decimal_choices_validator


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
    my_rate = serializers.SerializerMethodField()
    my_comment = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_average_rate(self, obj):
        if Rating.objects.filter(movie=obj).exists():
            return round(
                sum(map(lambda x: x.rate, Rating.objects.filter(movie=obj))) / len(Rating.objects.filter(movie=obj)), 1)
        return None

    def get_my_rate(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            if Rating.objects.filter(movie=obj, created_by=request.user).exists():
                my_rating = Rating.objects.get(movie=obj, created_by=request.user)
                context = dict()
                context['id'] = my_rating.id
                context['my_rate'] = my_rating.rate
                return context
        return None

    def get_my_comment(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            if Comment.objects.filter(movie=obj, created_by=request.user).exists():
                my_comment_obj = Comment.objects.get(movie=obj, created_by=request.user)
                serializer = CommentSerializer(my_comment_obj, context={'request': request})
                return serializer.data
        return None


class MovieListSerializer(serializers.ModelSerializer):
    average_rate = serializers.SerializerMethodField()
    my_rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        exclude = ('plot', 'runtime', 'screening')

    def get_average_rate(self, obj):
        if Rating.objects.filter(movie=obj).exists():
            return round(
                sum(map(lambda x: x.rate, Rating.objects.filter(movie=obj))) / len(Rating.objects.filter(movie=obj)), 1)
        return None

    def get_my_rate(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            if Rating.objects.filter(movie=obj, created_by=request.user).exists():
                my_rating = Rating.objects.get(movie=obj, created_by=request.user)
                context = dict()
                context['my_rate'] = my_rating.rate
                return context
        return None


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'created_by', 'rate', 'movie']
        extra_kwargs = {
            'created_by': {'required': False, 'allow_null': True},
            'movie': {'required': False, 'allow_null': True},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rate'].validators = [decimal_choices_validator]


class CarouselSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True)

    class Meta:
        model = Carousel
        fields = '__all__'
