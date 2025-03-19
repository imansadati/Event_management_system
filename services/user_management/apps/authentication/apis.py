from rest_framework.views import APIView
from apps.users.services import user_attendee_create
from rest_framework import serializers
from apps.users.models import AttendeeUser
from django.http import HttpRequest
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.apis import AttendeeUserDetailApi
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .services import authenticate_user


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

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        data = AttendeeUserDetailApi.OutputAttendeeSerializer(user).data
        data.update({
            'access_token': access_token,
            'refresh_token': str(refresh),
        })
        return Response(data=data)


class AttendeeLoginApi(APIView):
    class InputAttendeeLoginSerializer(serializers.Serializer):
        identifier = serializers.CharField(max_length=128, write_only=True)
        password = serializers.CharField(max_length=128, write_only=True)

    def post(self, request: HttpRequest):
        serializer = self.InputAttendeeLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate_user(**serializer.validated_data)

        if not user:
            raise AuthenticationFailed()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        data = AttendeeUserDetailApi.OutputAttendeeSerializer(user).data
        data.update({
            'access_token': access_token,
            'refresh_token': str(refresh),
        })
        return Response(data=data)
