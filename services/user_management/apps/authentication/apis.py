from rest_framework.views import APIView
from apps.users.services import user_attendee_create
from rest_framework import serializers
from apps.users.models import AttendeeUser
from django.http import HttpRequest
from apps.users.apis import AttendeeUserDetailApi
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .services import authenticate_user, generate_tokens


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

        tokens = generate_tokens(user)

        data = AttendeeUserDetailApi.OutputAttendeeSerializer(user).data
        data.update(tokens)
        return Response(data=data)
