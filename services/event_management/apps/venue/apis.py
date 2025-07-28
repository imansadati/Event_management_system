from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework import serializers
from .models import Venue
from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from .selectors import venue_list
from rest_framework.views import APIView


class VenueListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputVenueListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Venue
            fields = '__all__'

    class FilterVenueSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=128, required=False)
        city = serializers.CharField(max_length=100, required=False)

    def get(self, request: HttpRequest):
        filter_serializers = self.FilterVenueSerializer(
            data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)

        venues = venue_list(filters=filter_serializers.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputVenueListSerializer,
            queryset=venues,
            request=request,
            view=self
        )


class VenueGetwayApiViewset(ViewSet):
    def list(self, request: HttpRequest):
        return VenueListApi.as_view()(request._request)
