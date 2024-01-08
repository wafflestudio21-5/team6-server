from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import viewsets

from .serializers import *
from .models import WaffleUser

import os

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs).data
        access_token = response_data.get("access")
        refresh_token = response_data.get("refresh")

        # Modify the response data to only include the access token
        response_data = {"access": access_token}
        response = JsonResponse(response_data)
        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                samesite="None",
            )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs).data
        access_token = response_data.get("access")
        refresh_token = response_data.get("refresh")

        # Modify the response data to only include the access token
        response_data = {"access": access_token}
        response = JsonResponse(response_data)

        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,
                samesite="None",
            )

        return response


# authentication test
class MyProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Headers:", request.headers)
        response = JsonResponse({"message": "You are authenticated"})
        print("Response:", response.content.decode())
        return response


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = WaffleUser.objects.all()
    serializer_class = UserSerializer
