from rest_framework.views import APIView
from apps.users.services import user_attendee_create
from rest_framework import serializers, status
from apps.users.models import AttendeeUser
from django.http import HttpRequest
from apps.users.apis import AttendeeUserDetailApi
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from .services import (authenticate_user, blacklist_refreshtoken,
                       is_refreshtoken_blacklisted, update_password, generate_reset_password_token,
                       verify_reset_password_token)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from .selectors import get_user_by_id, get_user_by_email, get_user_by_email_and_id
from grpc_service.client.client import send_email_via_rpc
from .tokens import generate_jwt_tokens
from shared_utils.permissions import IsAuthenticatedViaJWT


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

        tokens = generate_jwt_tokens(user)

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

        send_email_via_rpc(
            user.email, 'wellcome', 'wellcome to our platform')

        tokens = generate_jwt_tokens(user)

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
                new_token = generate_jwt_tokens(user)
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


class ChangePasswordApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT]

    class InputChangePasswordSerializer(serializers.Serializer):
        old_password = serializers.CharField(write_only=True)
        new_password = serializers.CharField(min_length=6, write_only=True)
        confirm_password = serializers.CharField(min_length=6, write_only=True)

        # You can use the validate_password function to select a secure password in the new_password attr.
        def validate(self, attrs):
            if attrs['new_password'] != attrs['confirm_password']:
                raise ValidationError(
                    {'confirm_password': 'passwords do not match.'})
            return attrs

    def post(self, request: HttpRequest):
        serializer = self.InputChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        user = request.user

        # Get refresh token from cookie or request.
        refresh_token = request.COOKIES.get(
            'refresh') or request.data.get('refresh')

        if not refresh_token:
            raise ValidationError('Refresh token is required')

        if not user.check_password(old_password):
            raise ValidationError('Password is incorrect. try again.')

        try:
            refresh_token = RefreshToken(refresh_token)

            if not is_refreshtoken_blacklisted(refresh_token):
                update_password(user, new_password)

                blacklist_refreshtoken(refresh_token)
                return Response({"detail": "Password changed successfully. Please log in again."}, status=status.HTTP_200_OK)
            raise AuthenticationFailed(
                detail='Token is blacklisted. Please log in again.')

        except ExpiredTokenError:
            raise AuthenticationFailed(
                detail='Refresh token has expired. Please log in again.')
        except Exception as e:
            raise ValidationError(e)


# Respose to generates and send token to user.
class ForgotPasswordApi(APIView):
    class InputForgotSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=128)

    def post(self, request: HttpRequest):
        serializer = self.InputForgotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_by_email(**serializer.validated_data)

        if user:
            token = generate_reset_password_token(user)
            reset_url = f'http://localhost:8001/api/auth/reset-password?token={token}'

            send_email_via_rpc(recipient=user.email, subject='reset password process',
                               body=f'Click on this url to continue change password process: {reset_url}')
            print(reset_url)

        return Response({'detail': 'If this email exists, a reset link was sent.'})


# Response to validate token and reset password.
class ResetPasswordApi(APIView):
    class InputResetSerializer(serializers.Serializer):
        token = serializers.CharField(max_length=200)
        new_password = serializers.CharField(min_length=6)

    def post(self, request: HttpRequest):
        serializer = self.InputResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        payload = verify_reset_password_token(token)

        if not payload:
            raise ValidationError(
                detail='Invalid or expired token.', code=status.HTTP_400_BAD_REQUEST)

        user = get_user_by_email_and_id(
            id=payload['user_id'], email=payload['email'])

        if not user:
            raise NotFound(detail='User not found.',
                           code=status.HTTP_404_NOT_FOUND)

        update_password(user, new_password)

        return Response({"detail": "Password reset successful."})
