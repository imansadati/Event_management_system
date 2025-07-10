from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpRequest
from .models import Event
from .selectors import event_list, event_get
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status


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


class EventDetailApi(APIView):
    class OutputEventSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            exclude = ['type', 'status', 'published_at', 'updated_at']

    def get(self, request: HttpRequest, pk):
        event = event_get(pk)

        data = self.OutputEventSerializer(event).data

        return Response(data, status=status.HTTP_200_OK)


class EventGetwayApiViewSet(ViewSet):
    def list(self, request: HttpRequest):
        return EventListApi.as_view()(request._request)

    def retrieve(self, request: HttpRequest, pk=None):
        return EventDetailApi.as_view()(request._request, pk=pk)
