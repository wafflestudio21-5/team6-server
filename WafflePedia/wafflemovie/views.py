from django.shortcuts import render
from django.shortcuts import redirect
from .serializers import *
from rest_framework import viewsets
from .models import WaffleUser
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.naver import views as naver_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import requests
from rest_framework import status
from json.decoder import JSONDecodeError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

# 환경변수 사용
import os
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import *
import json
import jwt
from oauthlib.oauth2 import OAuth2Error


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
                httponly=True,  # Recommended for security
                samesite="None",  # Recommended for CSRF protection
            )

        print(response.content)
        print(response.cookies)
        print("\nHeader:", response.headers)

        # return JsonResponse(response_data)
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
                httponly=True,  # Recommended for security
                samesite="None",  # Recommended for CSRF protection
            )

        print(response.content)
        print(response.cookies)
        print("\nHeader:", response.headers)

        # return JsonResponse(response_data)
        return response


class MyProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Headers:", request.headers)
        response = JsonResponse({"message": "You are authenticated"})
        print("Response:", response.content.decode())
        return response


state = os.environ.get("STATE")
BASE_URL = "http://127.0.0.1:8000/"
GOOGLE_CALLBACK_URI = BASE_URL + "auth/google/callback/"
KAKAO_CALLBACK_URI = BASE_URL + "auth/kakao/callback/"
NAVER_CALLBACK_URI = BASE_URL + "auth/naver/callback/"


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
    print("\ncode:",code)
    state = "justrandomstring"

    #token 발급 요청
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    print("\naccess_token:", access_token)

    #email request
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
    print("\nemail:", email)


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

        response_data = JsonResponse(accept_json)
        content = response_data.content.decode('utf-8')  # Decode the response content
        data = json.loads(content)
        access_token=data.get("access")
        refresh_token = data.get("refresh")

        # Modify the response data to only include the access token
        response_data = {"access": access_token}
        response = JsonResponse(response_data)

        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,  # Recommended for security
                samesite="None",  # Recommended for CSRF protection
            )

        print("\nGoogle response content:",response.content)
        print("\nGoogle response cookies:",response.cookies)
        print("\nGoogle Header:", response.headers)

        # return JsonResponse(response_data)
        return response

    except WaffleUser.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}auth/google/login/finish/", data=data)
        print("\naccept.headers:",accept.headers)
        accept_status = accept.status_code
        if accept_status != 200:
            try:
                # The code that's causing the error
                accept_json = accept.json()
            except Exception as e:
                print("An error occurred:", e)

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

    response_data = JsonResponse(accept_json)
    content = response_data.content.decode('utf-8')  # Decode the response content
    data = json.loads(content)
    access_token=data.get("access")
    refresh_token = data.get("refresh")
    print("\nmy access_token:", access_token)
    print("\nmy refresh_token:", refresh_token)

    # Modify the response data to only include the access token
    response_data = {"access": access_token}
    response = JsonResponse(response_data)

    if refresh_token:
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,  # Recommended for security
            samesite="None",  # Recommended for CSRF protection
        )

    print("\nKakao response content:",response.content)
    print("\nKakao response cookies:",response.cookies)
    print("\nKakao Header:", response.headers)

    # return JsonResponse(response_data)
    return response

from allauth.socialaccount.providers.google.provider import GoogleProvider

class CustomGoogleOAuth2Adapter(google_view.GoogleOAuth2Adapter):
    provider_id = GoogleProvider.id
    access_token_url = "https://accounts.google.com/o/oauth2/token"
    authorize_url = "https://accounts.google.com/o/oauth2/auth"
    profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    def complete_login(self, request, app, token, **kwargs):
        print(request)
        resp = requests.get(
            self.profile_url,
            params={"access_token": token.token, "alt": "json"},
        )
        resp.raise_for_status()
        extra_data = resp.json()
        print("???")
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login


class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
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


def naver_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_NAVER_CLIENT_ID")
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&state={state}&redirect_uri={NAVER_CALLBACK_URI}"
    )


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
    print(token_response_json)
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

    email = profile_json.get("response").get("email")

    if email is None:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)


    try:
        user = User.objects.get(email=email)
        data = {'access_token': access_token, 'code': code}
        # accept 에는 token 값이 json 형태로 들어온다({"key"}:"token value")
        # 여기서 오는 key 값은 authtoken_token에 저장된다.
        accept = requests.post(
            f"{BASE_URL}auth/naver/login/finish/", data=data
        )
        # 만약 token 요청이 제대로 이루어지지 않으면 오류처리
        if accept.status_code != 200:
            return JsonResponse({"error": "Failed to Signin."}, status=accept.status_code)
        accept_json = accept.json()
        accept_json.pop("user", None)

        response_data = JsonResponse(accept_json)
        content = response_data.content.decode('utf-8')  # Decode the response content
        data = json.loads(content)
        access_token=data.get("access")
        refresh_token = data.get("refresh")
        print("\nmy access_token:", access_token)
        print("\nmy refresh_token:", refresh_token)

        # Modify the response data to only include the access token
        response_data = {"access": access_token}
        response = JsonResponse(response_data)

        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,  # Recommended for security
                samesite="None",  # Recommended for CSRF protection
            )

        print("\nNaver response content:",response.content)
        print("\nNaver response cookies:",response.cookies)
        print("\nNaver Header:", response.headers)

        # return JsonResponse(response_data)
        return response

    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}auth/naver/login/finish/", data=data
        )
        # 만약 token 요청이 제대로 이루어지지 않으면 오류처리
        if accept.status_code != 200:
            return JsonResponse({"error": "Failed to SignUp."}, status=accept.status_code)
        accept_json = accept.json()
        accept_json.pop("user", None)

        response_data = JsonResponse(accept_json)
        content = response_data.content.decode('utf-8')  # Decode the response content
        data = json.loads(content)
        access_token=data.get("access")
        refresh_token = data.get("refresh")
        print("\nmy access_token:", access_token)
        print("\nmy refresh_token:", refresh_token)

        # Modify the response data to only include the access token
        response_data = {"access": access_token}
        response = JsonResponse(response_data)

        if refresh_token:
            response.set_cookie(
                "refresh_token",
                refresh_token,
                httponly=True,  # Recommended for security
                samesite="None",  # Recommended for CSRF protection
            )

        print("\nNaver response content:",response.content)
        print("\nNaver response cookies:",response.cookies)
        print("\nNaver Header:", response.headers)

        # return JsonResponse(response_data)
        return response


class NaverLogin(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = NAVER_CALLBACK_URI
    client_class = OAuth2Client
