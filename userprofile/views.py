from django.shortcuts import render
from waffleAuth.models import WaffleUser
from content.models import Movie, Rating, State, People
from comment.models import Comment, Like
from django.db.models import Count, F
# Create your views here.
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView, RetrieveUpdateAPIView
from .serializers import StateSerializer, UserRatingSerializer, CommentSerializer, UserDetailSerializer, UserSerializer, UserDeleteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenBlacklistView
from django.http import JsonResponse, QueryDict
import requests
import os
import json
from .paginations import *


class UserDetailView(RetrieveAPIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    queryset = WaffleUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


class UserMyPageDetailView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


class UserMyPageDeleteView(DestroyAPIView, TokenBlacklistView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserDeleteSerializer

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.perform_destroy(instance)

    def perform_destroy(self, instance):
        user = WaffleUser.objects.get(id=self.request.user.id)
        user.delete()
        return self.post(self.request)

    def post(self, request, *args, **kwargs):
        org_refresh_token = request.COOKIES.get('refresh_token')
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data["refresh"] = org_refresh_token
        if isinstance(request.data, QueryDict):
            request.data._mutable = False
        super().post(request, *args, **kwargs)
        response_data = {"message": "tokens deleted"}
        response = JsonResponse(response_data)
        response.delete_cookie('refresh_token')
        return response


class KakaoTokenRefreshView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve your REST API KEY and USER_REFRESH_TOKEN
        # It's a good practice to store sensitive data like API keys in environment variables
        rest_api_key = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
        kakao_refresh_token = request.COOKIES.get('kakao_refresh_token')

        if not kakao_refresh_token:
            return Response({"error": "Missing kakao_refresh_token"}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://kauth.kakao.com/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "refresh_token",
            "client_id": rest_api_key,
            "refresh_token": kakao_refresh_token,
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:

            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse(response.json(), status=response.status_code, safe=False)

class KakaoUnlinkUserView(UserMyPageDeleteView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        return self.perform_destroy(instance)
    def perform_destroy(self, instance):
        user = WaffleUser.objects.get(id=self.request.user.id)
        user.delete()
        return self.post(self.request)

    def post(self, request, *args, **kwargs):
        user = request.user
        #token = request.auth
        kakao_refresh_token = request.COOKIES.get('kakao_refresh_token')
        token_refresh_view = KakaoTokenRefreshView()
        token_refresh_view.request = request
        token_refresh_view.args = args
        token_refresh_view.kwargs = kwargs
        kakao_refresh_response = token_refresh_view.get(request, *args, **kwargs)
        kakao_refresh_response_content = kakao_refresh_response.content  # Get the JSON string from the response
        kakao_refresh_response_json = json.loads(
            kakao_refresh_response_content)  # Deserialize the JSON string into a Python dictionary
        #print("\nkakao_refresh_response_json:", kakao_refresh_response_json)
        kakao_access_token = kakao_refresh_response_json.get("access_token")

        if not kakao_access_token:
            return Response({"error": "Token is missing or invalid"}, status=401)

        #print("\ntoken: ", kakao_access_token)
        headers = {
            "Authorization":f"Bearer {kakao_access_token}",
            #"Content-Type": "application/x-www-form-urlencoded",
        }

        url = "https://kapi.kakao.com/v1/user/unlink"
        response = requests.post(url, headers=headers)

        if response.status_code != 200:
            return JsonResponse(response.json(), status=response.status_code, safe=False)
        else:

            super().post(request, *args, **kwargs)
            return JsonResponse(response.json(), status=response.status_code, safe=False)
          

class AddFollowView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            loggedin_user = request.user  # Authenticated user from JWT token
            user_to_follow = WaffleUser.objects.get(pk=user_id)

            if loggedin_user == user_to_follow:
                return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            if user_to_follow in loggedin_user.following.all():
                return Response({"error": f"You already follow {user_to_follow.username}."},
                                status=status.HTTP_400_BAD_REQUEST)

            loggedin_user.following.add(user_to_follow)

            #print(f"User: {loggedin_user.username}")  # Print the user making the request
            #print("Following list:",
            #      [user.username for user in loggedin_user.following.all()])  # List of usernames being followed

            return Response({"message": f"Successfully followed the user {user_to_follow.username}."}, status=status.HTTP_200_OK)

        except WaffleUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UnfollowView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get user_id from request data
            user_id = request.data.get('user_id')
            if user_id is None:
                return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            loggedin_user = request.user  # Authenticated user from JWT token
            user_to_unfollow = WaffleUser.objects.get(pk=user_id)

            if loggedin_user == user_to_unfollow:
                return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            if user_to_unfollow not in loggedin_user.following.all():
                return Response({"error": f"You do not follow {user_to_unfollow.username}."},
                                status=status.HTTP_400_BAD_REQUEST)

            loggedin_user.following.remove(user_to_unfollow)  # Remove the user from the following list

            return Response({"message": f"Successfully unfollowed the user {user_to_unfollow.username}."}, status=status.HTTP_200_OK)

        except WaffleUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserFollowView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get user_id from request data
            user_id = request.data.get('user_id')
            if user_id is None:
                return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            loggedin_user = request.user  # Authenticated user from JWT token
            user_to_follow = WaffleUser.objects.get(pk=user_id)

            if loggedin_user == user_to_follow:
                return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            if user_to_follow in loggedin_user.following.all():
                return Response({"error": f"You already follow {user_to_follow.username}."},
                                status=status.HTTP_400_BAD_REQUEST)

            loggedin_user.following.add(user_to_follow)

            #print(f"User: {loggedin_user.username}")  # Print the user making the request
            #print("Following list:",
            #      [user.username for user in loggedin_user.following.all()])  # List of usernames being followed

            return Response({"message": f"Successfully followed the user {user_to_follow.username}."}, status=status.HTTP_200_OK)

        except WaffleUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FollowersListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.followers.all()


class FollowingsListView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user = WaffleUser.objects.get(pk=user_id)
        return user.following.all()


class UserCommentsListView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = RatingPagination

    def get_queryset(self):
        user_id = self.kwargs['pk']
        order_options = {
            'like': '-like_count',
            'high-rating': '-rate_count',
            'low-rating': 'rate_count',
            'created': '-created_at'
        }
        order_option = self.request.query_params.get('order')

        queryset = Comment.objects.filter(created_by_id=user_id).annotate(
            like_count=Count('likes'),
            reply_count=Count('reply_set')
        )

        queryset = queryset.order_by(order_options['like'])

        if order_option in order_options:
            if order_option in ['high-rating', 'low-rating']:
                queryset = queryset.filter(rating__isnull=False)
            queryset = queryset.order_by(order_options[order_option])

        return queryset


class UserRatingListView(ListAPIView):
    serializer_class = UserRatingSerializer
    pagination_class = RatingPagination

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        order_options = {
            'high-rating': '-rate',
            'low-rating': 'rate',
            'created': '-updated_at'
        }
        rate = self.request.query_params.get('rate')
        order_option = self.request.query_params.get('order')
        queryset = Rating.objects.filter(created_by_id=user_id)
        if rate is not None:
            queryset = queryset.filter(rate=rate)

        if order_option in order_options:
            queryset = queryset.order_by(order_options[order_option])
        else:
            queryset = queryset.order_by(order_options['created'])

        queryset = queryset.select_related('movie')

        return queryset


class UserMovieStateListView(ListAPIView):
    serializer_class = StateSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        user_state = self.kwargs.get("user_state")
        return State.objects.filter(user_id=user_id, user_state=user_state)


class UserLikedCommentsListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        liked_comments = Comment.objects.filter(likes__created_by=user)
        return liked_comments
