from rest_framework.views import APIView
from apps.users.services import user_attendee_create, user_staff_create, user_admin_create
from rest_framework import serializers, status
from apps.users.models import AttendeeUser
from django.http import HttpRequest
from apps.users.apis import AttendeeUserDetailApi
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError, NotFound
from .services import (authenticate_user, blacklist_token,
                       is_token_blacklisted, update_password, generate_specific_token,
                       verify_specific_token)
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

        send_email_via_rpc(
            user.email, 'wellcome', 'wellcome to our platform')

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

        if is_token_blacklisted(token=refresh_token, token_type='refresh_token_blacklist'):
            raise AuthenticationFailed(
                detail='Token is blacklisted. Please log in again.')

        try:
            token = RefreshToken(refresh_token)
            user_id = token['user_id']
            role = token['role']

            user = get_user_by_id(user_id, role)

            if user:
                blacklist_token(
                    token=refresh_token, token_type='refresh_token_blacklist', timelife='REFRESH')
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

        if is_token_blacklisted(token=refresh_token, token_type='logout_token_blacklist'):
            raise AuthenticationFailed(
                detail='Token is blacklisted. Please log in again.')

        try:
            token = RefreshToken(refresh_token)
            blacklist_token(
                token=token, token_type='logout_token_blacklist', timelife='REFRESH')
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

            if not is_token_blacklisted(token=refresh_token, token_type='changepass_token_blacklist'):
                update_password(user, new_password)

                blacklist_token(
                    token=refresh_token, token_type='changepass_token_blacklist', timelife='REFRESH')
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
            token = generate_specific_token(user=user, type='reset_password')
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

        if is_token_blacklisted(token_type='resetpass_token_blacklist', token=token):
            raise ValidationError('Token is blacklisted.')

        payload = verify_specific_token(token=token, type='reset_password')

        if not payload:
            raise ValidationError(
                detail='Invalid or expired token.', code=status.HTTP_400_BAD_REQUEST)

        user = get_user_by_email_and_id(
            id=payload['user_id'], email=payload['email'])

        if not user:
            raise NotFound(detail='User not found.',
                           code=status.HTTP_404_NOT_FOUND)

        update_password(user, new_password)

        blacklist_token(token_type='resetpass_token_blacklist', token=token)

        return Response({"detail": "Password reset successful."})


# Sent invite via email to invite new staff/admin
class InviteUserViaAdminApi(APIView):
    class InputInviteSerializer(serializers.Serializer):
        role = serializers.ChoiceField(
            choices=[('admin', 'Admin'), ('staff', 'Staff')])
        email = serializers.EmailField(max_length=128)

    def post(self, request: HttpRequest):
        serializer = self.InputInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        role = serializer.validated_data['role']
        email = serializer.validated_data['email']

        user = get_user_by_email(email)

        if user:
            raise ValidationError(
                detail='This user already exist.', code=status.HTTP_400_BAD_REQUEST)

        token = generate_specific_token(email, 'invite_user', role=role)
        invite_url = f'http://localhost:8001/api/auth/accept-invite?token={token}'

        send_email_via_rpc(recipient=email, subject='invite user',
                           body=f'Click on this url to continue change signup: {invite_url}')
        print(invite_url)

        return Response({'detail': 'If this email exists, a invite link was sent.'})


# validate and creation process
class AcceptInviteViaAdminApi(APIView):
    class InputAcceptSerializer(serializers.Serializer):
        full_name = serializers.CharField(max_length=128)
        username = serializers.CharField(max_length=128)
        password = serializers.CharField(min_length=6)
        work_experience = serializers.IntegerField(required=False)
        job_title = serializers.CharField(max_length=64, required=False)

    def post(self, request: HttpRequest):
        serializer = self.InputAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = request.GET.get('token')

        if is_token_blacklisted(token_type='invite_token_blacklist', token=token):
            raise ValidationError('Token is blacklisted.')

        payload = verify_specific_token(token, type='invite_user')

        if not payload:
            raise ValidationError(
                detail='Invalid or expired token.', code=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.get('username')
        full_name = serializer.validated_data.get('full_name')
        password = serializer.validated_data.get('password')

        role = payload['role']
        email = payload['email']

        if role == 'staff':
            job_title = serializer.validated_data.get('job_title')
            work_experience = serializer.validated_data.get('work_experience')
            user_staff_create(email=email, username=username, password=password,
                              full_name=full_name, job_title=job_title, work_experience=work_experience)
        else:
            user_admin_create(email=email, username=username,
                              password=password, full_name=full_name)

        blacklist_token(token_type='invite_token_blacklist',
                        token=token, timelife='ACCESS')

        return Response({'detail': 'Account created successfully. now you can login.'})
