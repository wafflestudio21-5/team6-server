from django.contrib import admin
from django.urls import path, include
from rest_framework import urls
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('list', UserViewSet)  # 유저리스트 (테스트용)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("allauth.urls")),
    path('auth/google/login', google_login, name='google_login'),
    path('auth/google/callback/', google_callback, name='google_callback'),
    path('auth/google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
]
