from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *
from rest_framework import routers

# 유저리스트 (테스트용)
router = routers.DefaultRouter()
router.register("list", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # for login/logout
    path("auth/", include("dj_rest_auth.urls")),
    # for registration
    path("auth/register/", include("dj_rest_auth.registration.urls")),
    # path("auth/", include("allauth.urls")),
    # Google
    path("auth/google/login/", google_login, name="google_login"),
    path("auth/google/callback/", google_callback, name="google_callback"),
    path(
        "auth/google/login/finish/", GoogleLogin.as_view(), name="google_login_todjango"
    ),
    # Kakao
    path("auth/kakao/login/", kakao_login, name="kakao_login"),
    path("auth/kakao/callback/", kakao_callback, name="kakao_callback"),
    path("auth/kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"),
]
