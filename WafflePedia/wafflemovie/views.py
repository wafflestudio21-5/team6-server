from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.views import APIView
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# from django.conf import settings
from .models import WaffleUser
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status
from json.decoder import JSONDecodeError

# 환경변수 사용
import os, environ
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response_data = super().post(request, *args, **kwargs).data
        response = JsonResponse(response_data)

        access_token = response_data.get('access')
        refresh_token = response_data.get('refresh')
        print(request.headers)
        #print("Access Token:", access_token)  # Temporary print statement
        #print("Refresh Token:", refresh_token)

        if access_token:
                response.set_cookie(
                    'access_token',
                    access_token,
                    httponly=True,  # Recommended for security
                    samesite='Lax'  # Recommended for CSRF protection
                )

        if refresh_token:
            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=True,  # Recommended for security
                samesite='Lax'  # Recommended for CSRF protection
            )

        return response



# class CookieTokenRefreshView(TokenRefreshView):
#     def post(self, request, *args, **kwargs):
#         # The refresh token is automatically included in request.COOKIES
#         request.data['refresh'] = request.COOKIES.get('refresh_token')
#         return super().post(request, *args, **kwargs)






state = os.environ.get("STATE")
BASE_URL = "http://127.0.0.1:8000/"
GOOGLE_CALLBACK_URI = BASE_URL + "auth/google/callback/"
KAKAO_CALLBACK_URI = BASE_URL + "auth/kakao/callback/"


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


def google_callback(request):
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get("code")
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    email_req_json = email_req.json()
    email = email_req_json.get("email")
    """
    Signup or Signin Request
    """
    try:
        user = WaffleUser.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "google":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 Google로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}auth/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)
    except WaffleUser.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}auth/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)


def kakao_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


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
    accept_status = accept.status_code
    if accept_status != 200:
        return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
    accept_json = accept.json()
    accept_json.pop("user", None)
    return JsonResponse(accept_json)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = WaffleUser.objects.all()
    serializer_class = UserSerializer
