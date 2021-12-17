from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from bonfix_utils.utils import logger
from .models import UserProfile, AccountActivationCode
from .models import User

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("name",)


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ("email", "password", "profile")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            UserProfile.objects.create(user=user, name=profile_data["name"])
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            try:
                user = User.objects.get(email=email)
            except:
                raise serializers.ValidationError(
                    "A user with this email and password is not found."
                )
            if user.is_active == 0:
                raise serializers.ValidationError(
                {'error_code': "ACCOUNT_NOT_ACTIVATED", 'error_message': "You need to activate your account in order to login."}
                )
            else:
                raise serializers.ValidationError(
                    "Wrong password or email. Please try again"
                )

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email and password does not exists"
            )
        return {"email": user.email, "token": jwt_token}


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "profile")


class AccountActivationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    verification_code = serializers.CharField(max_length=10)
    status = serializers.IntegerField(required=False)

    class Meta:
        model = AccountActivationCode
        fields = ['verification_code', 'email', 'status']

    def validate(self, data):
        # AccountActivationCode
        email = data.get("email", None)
        code = data.get("verification_code", None)

        try:
            aac = AccountActivationCode.objects.get(email=email, verification_code=code)
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            return aac
        except:
            raise serializers.ValidationError(
                "Verification failed. Wrong verification code!"
            )