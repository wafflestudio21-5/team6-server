from rest_framework import serializers
from waffleAuth.models import WaffleUser
from content.models import Movie, Rating, State
from comment.models import Comment, Like


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    comment_num = serializers.SerializerMethodField(read_only=True)
    rate_num = serializers.SerializerMethodField(read_only=True)
    liked_comment_num = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WaffleUser
        fields = ['id', 'username', 'nickname', 'bio', 'profile_photo',
                  'background_photo', 'followers_count', 'following_count',
                  'comment_num', 'rate_num', 'liked_comment_num']

    def get_rate_num(self, obj):
        return Rating.objects.filter(created_by=obj).count()

    def get_comment_num(self, obj):
        return Comment.objects.filter(created_by=obj).count()

    def get_liked_comment_num(self, obj):
        return Comment.objects.filter(likes__created_by=obj).count()
      

class UserSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = WaffleUser
        fields = ['id', 'username', 'nickname', 'profile_photo', 'background_photo']


class MovieSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['movieCD', 'title_ko', 'poster', 'release_date']


class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    comment_num = serializers.SerializerMethodField(read_only=True)
    rate_num = serializers.SerializerMethodField(read_only=True)
    liked_comment_num = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WaffleUser
        fields = ['id', 'username', 'nickname', 'bio', 'profile_photo',
                  'background_photo', 'followers_count', 'following_count',
                  'comment_num', 'rate_num', 'liked_comment_num']

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        instance.background_photo = validated_data.get('background_photo', instance.background_photo)
        instance.save()
        return instance

    def get_rate_num(self, obj):
        return Rating.objects.filter(created_by=obj).count()

    def get_comment_num(self, obj):
        return Comment.objects.filter(created_by=obj).count()

    def get_liked_comment_num(self, obj):
        return Comment.objects.filter(likes__created_by=obj).count()


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaffleUser
        fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    created_by = UserSummarySerializer()
    movie = MovieSummarySerializer()

    class Meta:
        model = Comment
        fields = [
            'id', 'created_by', 'movie', 'content', 'rating', 'created_at',
            'updated_at', 'like_count', 'reply_count'
        ]
        depth = 1 #영화 정보 보여주기

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_reply_count(self, obj):
        return obj.replies.count()


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
