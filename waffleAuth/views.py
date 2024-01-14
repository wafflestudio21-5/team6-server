from django.shortcuts import redirect
from .serializers import *
from rest_framework import viewsets
from .models import WaffleUser
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.naver import views as naver_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import requests
from json.decoder import JSONDecodeError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

import os
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView
from django.http import JsonResponse
import json


from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import LoginView
from dj_rest_auth.app_settings import api_settings


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    def get_response_data(self, user):
        response_data = super().get_response_data(user)

        if api_settings.USE_JWT and hasattr(self, 'refresh_token'):
            try:
                # Blacklist the refresh token
                self.refresh_token.blacklist()
            except Exception as e:
                pass

        return response_data


# token
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs).data
        access_token = response_data.get("access")
        refresh_token = response_data.get("refresh")

        # response가 access token만 포함하도록 변경
        response_data = {"access": access_token}
        response = JsonResponse(response_data)
        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly="False",
                samesite="None",
                secure=True,
                domain=".wafflepedia.xyz",
            )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs).data
        access_token = response_data.get("access")
        refresh_token = response_data.get("refresh")

        # response가 access token만 포함하도록 변경
        response_data = {"access": access_token}
        response = JsonResponse(response_data)

        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly="False",
                samesite="None",
                secure=True,
                domain=".wafflepedia.xyz",
            )

        return response


# social login
state = os.environ.get("STATE")
BASE_URL = os.environ.get("BASE_URL")
KAKAO_CALLBACK_URI = BASE_URL + "auth/kakao/callback/"
NAVER_CALLBACK_URI = BASE_URL + "auth/naver/callback/"
REDIRECT_URI = BASE_URL + "auth/"


def kakao_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def naver_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_NAVER_CLIENT_ID")
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&state={state}&redirect_uri={NAVER_CALLBACK_URI}"
    )


def set_response(accept):
    accept_status = accept.status_code
    # not accepted
    if accept_status != 200:
        return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)

    # accepted
    accept_json = accept.json()
    accept_json.pop("user", None)
    response_data = JsonResponse(accept_json)
    content = response_data.content.decode("utf-8")
    data = json.loads(content)
    access_token = data.get("access")
    refresh_token = data.get("refresh")

    # response가 access token만 포함하도록 변경
    response_data = {"access": access_token}
    response = JsonResponse(response_data)

    if refresh_token:
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly="False",
            samesite="None",
            secure=True,
            domain=".wafflepedia.xyz",
        )

    return response


def kakao_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    code = request.GET.get("code")

    # code로 access token 요청
    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )
    token_response_json = token_request.json()

    # 에러 발생 시 중단
    error = token_response_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_response_json.get("access_token")

    # access token으로 카카오톡 프로필 요청
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()

    kakao_account = profile_json.get("kakao_account")

    data = {"access_token": access_token, "code": code}
    accept = requests.post(f"{BASE_URL}auth/kakao/login/finish/", data=data)

    return set_response(accept)


def naver_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_NAVER_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_NAVER_SECRET")
    code = request.GET.get("code")
    state_string = request.GET.get("state")

    # code로 access token 요청
    token_request = requests.get(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state_string}"
    )
    token_response_json = token_request.json()
    error = token_response_json.get("error", None)
    if error is not None:
        raise JSONDecodeError(error)

    access_token = token_response_json.get("access_token")

    # access token으로 네이버 프로필 요청
    profile_request = requests.post(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()

    data = {"access_token": access_token, "code": code}
    accept = requests.post(f"{BASE_URL}auth/naver/login/finish/", data=data)
    return set_response(accept)

    # email 비교 로직
    # email = profile_json.get("response").get("email")

    # if email is None:
    #     return JsonResponse(
    #         {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
    #     )

    # try:
    #     user = User.objects.get(email=email)
    #     data = {"access_token": access_token, "code": code}
    #     accept = requests.post(f"{BASE_URL}auth/naver/login/finish/", data=data)
    #     return set_response(accept)
    #
    # except User.DoesNotExist:
    #     data = {"access_token": access_token, "code": code}
    #     accept = requests.post(f"{BASE_URL}auth/naver/login/finish/", data=data)
    #     return set_response(accept)


class KakaoLogout(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
        redirect(
            f"https://kauth.kakao.com/oauth/logout?client_id={client_id}&logout_redirect_uri={REDIRECT_URI}"
        )

        return response


class NaverLogout(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        client_id = os.environ.get("SOCIAL_AUTH_NAVER_CLIENT_ID")
        client_secret = os.environ.get("SOCIAL_AUTH_NAVER_SECRET")
        access_token = request.GET.get("access_token")
        redirect(
            f"https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id={client_id}&client_secret={client_secret}&access_token={access_token}&service_provider=NAVER"
        )

        return response

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client


class NaverLogin(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = NAVER_CALLBACK_URI
    client_class = OAuth2Client


# authentication test
class MyProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = JsonResponse({"message": "You are authenticated"})
        return response


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = WaffleUser.objects.all()
    serializer_class = UserSerializer
