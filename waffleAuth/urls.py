from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView

# 유저리스트 (테스트용)
router = routers.DefaultRouter()
router.register("list", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # test
    path("test/", MyProtectedView.as_view()),
    # for token authentication
    path("", include("dj_rest_auth.urls")),
    path("token/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),

    path(
        "token/refresh/new/",
        CookieTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("token/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # for registration
    path("token/register/", CustomRegisterView.as_view(), name='custom-register'),
    # Kakao
    path("kakao/login/", kakao_login, name="kakao_login"),
    path("kakao/callback/", kakao_callback, name="kakao_callback"),
    path("kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"),
    path("kakao/logout/", KakaoLogout.as_view(), name="kakao_logout"),
    # Naver
    path("naver/login/", naver_login, name="naver_login"),
    path("naver/callback/", naver_callback, name="naver_callback"),
    path("naver/login/finish/", NaverLogin.as_view(), name="naver_login_todjango"),
    path("naver/logout/", NaverLogout.as_view(), name="naver_logout"),
]
