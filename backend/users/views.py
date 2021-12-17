import string
import random

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from bonfix_utils.utils import util_send_email
from .serializers import UserRegistrationSerializer, AccountActivationSerializer
from .serializers import UserLoginSerializer, UserDetailSerializer
from .models import UserProfile, AccountActivationCode
# import requests

from .tokens import TokenGenerator


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # create an email verification
        self.send_verification_mail(user)

        response = {
            "success": True,
            "status code": status.HTTP_200_OK,
            "message": "User registered successfully",
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def send_verification_mail(self, user):
        account_activation_token = TokenGenerator()
        current_site = get_current_site(self.request)
        name = user.email.split('@')[0]
        mail_subject = 'Activate your account.'
        # generate AccountActivationCode
        verification_code = self.generate_verification_code(5)
        aac = AccountActivationCode()
        aac.email = user.email
        aac.verification_code = verification_code
        aac.save()
        # create msg
        html_message = render_to_string('account_activation_email_template.html', {
            'user': user,
            'name': name,
            'verification_code': verification_code,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        plain_message = render_to_string('account_activation_email_template_plain.html', {
            'user': user,
            'name': name,
            'verification_code': verification_code,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        return util_send_email(mail_subject, [user.email], plain_message, html_message)
        # Or click on the link below to confirm your registration,
        # http://{{ domain }}{% url 'activate' uidb64=uid token=token %}

    def generate_verification_code(self, length):
        return ''.join(random.SystemRandom().choice(string.digits) for _ in range(length))


class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "email": serializer.data["email"],
            "token": serializer.data["token"],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserVerificationView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AccountActivationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "success": True,
            "status code": status.HTTP_200_OK,
            "email": serializer.data["email"],
            "message": "Account verification successful"
        }
        response.update(serializer.data)
        # serializer.data["token"]
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


# class UserView(RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserDetailSerializer
#
#     def get(self, request, email):
#         serializer = UserDetailSerializer(request.user)
#         return Response(serializer.data)


class UserProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                "success": True,
                "status code": status_code,
                "message": "User profile fetched successfully",
                "data": [
                    {
                        "name": user_profile.name,
                    }
                ],
            }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                "success": False,
                "status code": status.HTTP_400_BAD_REQUEST,
                "message": "User does not exists",
                "error": str(e),
            }
        return Response(response, status=status_code)
