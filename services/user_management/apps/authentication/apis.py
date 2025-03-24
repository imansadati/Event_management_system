from rest_framework.views import APIView
from apps.users.services import user_attendee_create
from rest_framework import serializers, status
from apps.users.models import AttendeeUser
from django.http import HttpRequest
from apps.users.apis import AttendeeUserDetailApi
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from jwt.exceptions import ExpiredSignatureError
from .services import authenticate_user, generate_tokens, refreshtoken_blacklist_processing
from .redis_client import redis_client


# just attendees can signup themselves as regular user. for other type of users admin must create. admin -> staff
class AttendeeRegisterApi(APIView):
    class InputAttendeeSignup(serializers.ModelSerializer):
        password = serializers.CharField(
            max_length=128, min_length=6, write_only=True)

        class Meta:
            model = AttendeeUser
            fields = ['username', 'email', 'full_name', 'password']

    def post(self, request: HttpRequest):
        serializer = self.InputAttendeeSignup(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_attendee_create(**serializer.validated_data)

        tokens = generate_tokens(user)

        data = AttendeeUserDetailApi.OutputAttendeeSerializer(user).data
        data.update(tokens)
        return Response(data=data)


class LoginApi(APIView):
    class InputLoginSerializer(serializers.Serializer):
        identifier = serializers.CharField(max_length=128, write_only=True)
        password = serializers.CharField(max_length=128, write_only=True)

    def post(self, request: HttpRequest):
        serializer = self.InputLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate_user(**serializer.validated_data)

        if not user:
            raise AuthenticationFailed()

        tokens = generate_tokens(user)

        data = AttendeeUserDetailApi.OutputAttendeeSerializer(user).data
        data.update(tokens)
        return Response(data=data)


class CustomRefreshTokenApi(APIView):
    def post(self, request: HttpRequest):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            raise ValidationError(detail='Refresh token is required.')

        if redis_client.get(f'blacklist:{refresh_token}'):
            raise AuthenticationFailed(
                detail='Token is blacklisted. Please log in again.')
