from rest_framework.views import APIView
from rest_framework import serializers
from .models import Organizer
from django.http import HttpRequest
from rest_framework.response import Response
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from .selectors import organizer_list
from rest_framework.viewsets import ViewSet


# CRUD
class OrganizerListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputOrganizerListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organizer
            fields = '__all__'

    class FilterOrganizerSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=128, required=False)

    def get(self, request: HttpRequest):
        filter_serializers = self.FilterOrganizerSerializer(
            data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)

        organizers = organizer_list(filters=filter_serializers.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputOrganizerListSerializer,
            queryset=organizers,
            request=request,
            view=self
        )


class OrganizerGetwayApiViewset(ViewSet):
    def list(self, request: HttpRequest):
        return OrganizerListApi.as_view()(request._request)
