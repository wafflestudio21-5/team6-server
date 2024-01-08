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
    # for token authentication
    path("", include("dj_rest_auth.urls")),
    path("token/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "token/refresh/new/",
        CookieTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # for registration
    path("register/", include("dj_rest_auth.registration.urls")),
]
