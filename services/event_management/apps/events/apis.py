from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpRequest
from .models import Event, EventCategory
from .selectors import event_list, event_get
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from .services import event_create
from rest_framework.exceptions import ValidationError


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


class EventCreateApi(APIView):
    class InputEventSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            exclude = ['status', 'created_at', 'updated_at']
            extra_kwargs = {'category': {'required': True}}
            extra_kwargs = {'published_at': {'required': True}}

        def validate(self, data):
            if data['start_datetime'] >= data['end_datetime']:
                raise ValidationError(
                    {'start_datetime': 'start_datetime must be before end_datetime'}
                )
            if data.get('type') not in ['public', 'private', 'invite_only']:
                raise ValidationError({'type': 'Invalid event type'})

            return data

    def post(self, reqeust: HttpRequest):
        serializer = self.InputEventSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)

        event = event_create(**serializer.validated_data)

        data = EventDetailApi.OutputEventSerializer(event).data
        return Response(data, status=status.HTTP_201_CREATED)


class EventUpdateApi(APIView):
    class InputEventSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = ['title', 'capacity']  # add more if needed

    def post(self, request: HttpRequest):
        pass


class EventGetwayApiViewSet(ViewSet):
    def list(self, request: HttpRequest):
        return EventListApi.as_view()(request._request)

    def retrieve(self, request: HttpRequest, pk=None):
        return EventDetailApi.as_view()(request._request, pk=pk)

    def create(self, request: HttpRequest):
        return EventCreateApi.as_view()(request._request)

    def update(self, request: HttpRequest, pk=None):
        return EventCreateApi.as_view()(request._request, pk=None)

    def partial_update(self, request: HttpRequest, pk=None):
        return EventCreateApi.as_view()(request._request, pk=None)
