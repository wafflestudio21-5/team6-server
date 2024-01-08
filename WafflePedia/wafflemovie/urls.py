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
    # test
    path("test/", MyProtectedView.as_view()),
    # for login/logout
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/token/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/new/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    # for registration
    path("auth/register/", include("dj_rest_auth.registration.urls")),
    # path("auth/", include("allauth.urls")),
    # Google
    path("auth/google/login/", google_login, name="google_login"),
    path("auth/google/callback/", google_callback, name="google_callback"),
    path("auth/google/login/finish/", GoogleLogin.as_view(), name="google_login_todjango"),
    # Kakao
    path("auth/kakao/login/", kakao_login, name="kakao_login"),
    path("auth/kakao/callback/", kakao_callback, name="kakao_callback"),
    path("auth/kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"),
    #Naver
    path('naver/login', naver_login, name='naver_login'),
    path('naver/callback/', naver_callback, name='naver_callback'),
    path('naver/login/finish/', NaverLogin.as_view(), name='naver_login_todjango'),
]
