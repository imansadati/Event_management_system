from rest_framework.views import APIView
from rest_framework import serializers
from .models import AdminUser
from django.http import HttpRequest
from .selectors import user_admin_list
from rest_framework.response import Response


class AdminUserListApi(APIView):
    class OutputAdminSerializer(serializers.ModelSerializer):
        class Meta:
            model = AdminUser
            fields = '__all__'

    def get(self, request: HttpRequest):
        users = user_admin_list()
        serializer = self.OutputAdminSerializer(users, many=True).data
        return Response(serializer)
