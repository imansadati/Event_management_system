from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpRequest
from .models import Event
from .selectors import event_list
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination


class EventListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputEventListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = '__all__'

    class FilterEventSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=128, required=False)
        type = serializers.CharField(max_length=16, required=False)

    def get(self, request: HttpRequest):
        filter_serializers = self.FilterEventSerializer(
            data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)

        events = event_list(filters=filter_serializers.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputEventListSerializer,
            queryset=events,
            request=request,
            view=self
        )


class EventGetwayApiViewSet(ViewSet):
    def list(self, request):
        return EventListApi.as_view()(request._request)
