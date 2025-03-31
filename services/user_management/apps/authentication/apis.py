from rest_framework.views import APIView
from apps.users.services import user_attendee_create
from rest_framework import serializers, status
from apps.users.models import AttendeeUser
from django.http import HttpRequest
from apps.users.apis import AttendeeUserDetailApi
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .services import authenticate_user, generate_tokens, blacklist_refreshtoken, is_refreshtoken_blacklisted
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from .selectors import get_user_by_id


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

        data = {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'tokens': tokens
        }
        return Response(data=data)


class CustomRefreshTokenApi(APIView):
    def post(self, request: HttpRequest):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            raise ValidationError(detail='Refresh token is required.')

        if is_refreshtoken_blacklisted(refresh_token):
            raise AuthenticationFailed(
                detail='Token is blacklisted. Please log in again.')

        try:
            token = RefreshToken(refresh_token)
            user_id = token['user_id']
            user = get_user_by_id(user_id)

            if user:
                blacklist_refreshtoken(refresh_token)
                new_token = generate_tokens(user)
                return Response({
                    'access_token': new_token['access_token'],
                    'refresh_token': new_token['refresh_token']
                }, status=status.HTTP_200_OK)

            raise AuthenticationFailed()
        except ExpiredTokenError:
            raise AuthenticationFailed(
                detail='Refresh token has expired. Please log in again.')


class LogoutApi(APIView):
    def post(self, request: HttpRequest):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            raise ValidationError('Refresh token is required')

        if is_refreshtoken_blacklisted(refresh_token):
            raise AuthenticationFailed(
                detail='Token is blacklisted. Please log in again.')

        try:
            token = RefreshToken(refresh_token)
            blacklist_refreshtoken(token)
            return Response({"message": "Successfully logged out."}, status=200)

        except ExpiredTokenError:
            raise AuthenticationFailed(
                detail='Refresh token has expired. Please log in again.')
