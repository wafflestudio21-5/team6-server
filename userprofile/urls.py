from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *


urlpatterns = [
    path('mypage/', UserMyPageDetailView.as_view(), name='user-detail'),
    path('mypage/delete/', UserMyPageDeleteView.as_view(), name='user-delete'),
    path('mypage/image_update/', UserMyPageImageDetailView.as_view(), name='user-image-update'),
    path('mypage/likes/comments/', UserLikedCommentsListView.as_view(), name='user-liked-comments'),
    path('mypage/delete/kakao_unlink/', KakaoUnlinkUserView.as_view(), name='kakao_unlink'),
    path('mypage/kakao_token_refresh/', KakaoTokenRefreshView.as_view(), name='kakao_token_refresh'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='user-followers'),
    path('<int:user_id>/followings/', FollowingsListView.as_view(), name='user-following'),
    path('<int:user_id>/add/follow/', AddFollowView.as_view(), name='user-add-follow-by-detail-page'),
    path('unfollow/', UnfollowView.as_view(), name='unfollow'),
    path('add/follow/', UserFollowView.as_view(), name='user-add-follow-by-userid'),
    path('<int:pk>/comments/', UserCommentsListView.as_view(), name='user-comments'),
    path('<int:user_id>/ratings/', UserRatingListView.as_view(), name='user-ratings'),
    path('<int:user_id>/movies/watching/', UserMovieStateListView.as_view(), {'user_state': 'watching'}, name='user-watching-movies'),
    path('<int:user_id>/movies/want_to_watch/', UserMovieStateListView.as_view(), {'user_state': 'want_to_watch'}, name='user-want-to-watch-movies'),
    path('<int:user_id>/movies/not_interested/', UserMovieStateListView.as_view(), {'user_state': 'not_interested'}, name='user-not-interested-movies'),
    ]
