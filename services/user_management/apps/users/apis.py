from rest_framework.views import APIView
from rest_framework import serializers
from .models import AdminUser
from django.http import HttpRequest
from .selectors import user_admin_list
# read ./shared_utils/README.md
from shared_utils.pagination import LimitOffsetPagination, get_paginated_response


class AdminUserListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        full_name = serializers.CharField(max_length=128, required=False)
        is_admin = serializers.BooleanField(
            allow_null=True, default=None, required=False)
        username = serializers.CharField(max_length=128, required=False)

    class OutputAdminSerializer(serializers.ModelSerializer):
        class Meta:
            model = AdminUser
            fields = '__all__'

    def get(self, request: HttpRequest):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_admin_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputAdminSerializer,
            queryset=users,
            request=request,
            view=self
        )
