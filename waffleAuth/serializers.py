from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account import app_settings as allauth_account_settings
from allauth.utils import get_username_max_length
from allauth.account.adapter import get_adapter

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "nickname",
            "bio",
            "profile_photo",
            "background_photo",
            "following",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance


class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=True,
    )
    nickname = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=True,
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'password1': self.validated_data.get('password1', ''),
        }

    #clean_nickname 오버라이딩 필요 => username validation 참고

    # def validate_username(self, username):
    #     username = get_adapter().clean_username(username)
    #     return username

    # def clean_username(self, username, shallow=False):
    #     """
    #     Validates the username. You can hook into this if you want to
    #     (dynamically) restrict what usernames can be chosen.
    #     """
    #     for validator in app_settings.USERNAME_VALIDATORS:
    #         validator(username)
    #
    #     # TODO: Add regexp support to USERNAME_BLACKLIST
    #     username_blacklist_lower = [
    #         ub.lower() for ub in app_settings.USERNAME_BLACKLIST
    #     ]
    #     if username.lower() in username_blacklist_lower:
    #         raise forms.ValidationError(self.error_messages["username_blacklisted"])
    #     # Skipping database lookups when shallow is True, needed for unique
    #     # username generation.
    #     if not shallow:
    #         from .utils import filter_users_by_username
    #
    #         if filter_users_by_username(username).exists():
    #             user_model = get_user_model()
    #             username_field = app_settings.USER_MODEL_USERNAME_FIELD
    #             error_message = user_model._meta.get_field(
    #                 username_field
    #             ).error_messages.get("unique")
    #             if not error_message:
    #                 error_message = self.error_messages["username_taken"]
    #             raise forms.ValidationError(
    #                 error_message,
    #                 params={
    #                     "model_name": user_model.__name__,
    #                     "field_label": username_field,
    #                 },
    #             )
    #     return username


    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.nickname = self.cleaned_data['nickname']
        user.save()
        self.custom_signup(request, user)
        return user
