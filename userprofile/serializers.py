from rest_framework import serializers
from waffleAuth.models import WaffleUser
from content.models import Movie, Rating, State
from comment.models import Comment, Like


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = WaffleUser
        fields = ['id', 'username', 'nickname', 'bio', 'profile_photo', 'background_photo', 'followers_count', 'following_count']



class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = WaffleUser
        fields = ['id', 'username', 'nickname', 'bio', 'profile_photo', 'background_photo', 'followers_count', 'following_count']

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.bio = validated_data.get('bio', instance.bio)
        #instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        #instance.background_photo = validated_data.get('background_photo', instance.background_photo)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'movie', 'content', 'rating', 'created_at', 'updated_at', 'likes_count', 'reply_count']
        depth = 1 #영화 정보 보여주기

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_reply_count(self, obj):
        return obj.reply_set.count()

# serializers.py
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'movieCD', 'title_ko', 'title_original', 'plot', 'runtime',
            'prod_country', 'poster', 'release_date', 'cumulative_audience',
            'screening'
        ]


class UserRatingSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'rate', 'movie']
        depth = 1  # 영화 정보 보여주기


class StateSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = State
        fields = ['id', 'movie', 'user_state']
        extra_kwargs = {
            'user_state': {'read_only': True}
        }

    def to_representation(self, instance):
        representation = super(StateSerializer, self).to_representation(instance)
        representation['user_state_display'] = instance.get_user_state_display()
        return representation
