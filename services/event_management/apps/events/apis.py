from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpRequest
from .models import Event, EventCategory
from .selectors import event_list, event_get, event_category_list, event_category_get
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from .services import event_create, event_update, event_category_create, event_category_update
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

        # check the user does not enter additional fields
        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def put(self, request: HttpRequest, pk):
        return self.update_event(request, pk)

    def patch(self, request: HttpRequest, pk):
        return self.update_event(request, pk)

    def update_event(self, request: HttpRequest, pk):
        serializer = self.InputEventSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        event = event_get(pk)
        try:
            updated_event = event_update(
                event=event, data=serializer.validated_data)
            return Response(EventDetailApi.OutputEventSerializer(updated_event).data, status=status.HTTP_200_OK)
        except Exception as e:
            if e.get_codes() == ['no_content']:
                return Response({'detail': 'No changes detected. event data remains the same.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteApi(APIView):
    def delete(self, reqeust: HttpRequest, pk):
        event = event_get(pk)

        event.delete()

        return Response({'detail': f'This event with {pk} id successfully deleted.'}, status=status.HTTP_200_OK)


class EventGetwayApiViewSet(ViewSet):
    def list(self, request: HttpRequest):
        return EventListApi.as_view()(request._request)

    def retrieve(self, request: HttpRequest, pk=None):
        return EventDetailApi.as_view()(request._request, pk=pk)

    def create(self, request: HttpRequest):
        return EventCreateApi.as_view()(request._request)

    def update(self, request: HttpRequest, pk=None):
        return EventUpdateApi.as_view()(request._request, pk=pk)

    def partial_update(self, request: HttpRequest, pk=None):
        return EventUpdateApi.as_view()(request._request, pk=pk)

    def delete(self, request: HttpRequest, pk=None):
        return EventDeleteApi.as_view()(request._request, pk=pk)


class EventCategoryListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputEventCategoryListSerializer(serializers.ModelSerializer):
        class Meta:
            model = EventCategory
            fields = '__all__'

    class FilterEventCategorySerializer(serializers.Serializer):
        title = serializers.CharField(max_length=64, required=False)

    def get(self, request: HttpRequest):
        filter_serializers = self.FilterEventCategorySerializer(
            data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)

        categories = event_category_list(
            filters=filter_serializers.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputEventCategoryListSerializer,
            queryset=categories,
            request=request,
            view=self
        )


class EventCategoryDetailApi(APIView):
    class OutputEventCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = EventCategory
            exclude = ['created_at', 'updated_at']

    def get(self, request: HttpRequest, pk):
        category = event_category_get(pk)

        data = self.OutputEventCategorySerializer(category).data

        return Response(data, status=status.HTTP_200_OK)


class EventCategoryCreateApi(APIView):
    class InputEventCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = EventCategory
            fields = '__all__'

        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def post(self, reqeust: HttpRequest):
        serializer = self.InputEventCategorySerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)

        category = event_category_create(**serializer.validated_data)

        data = EventCategoryDetailApi.OutputEventCategorySerializer(
            category).data
        return Response(data, status=status.HTTP_201_CREATED)


class EventCategoryUpdateApi(APIView):
    class InputEventCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = EventCategory
            fields = ['title']

        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def put(self, request: HttpRequest, pk):
        return self.update_event_category(request, pk)

    def patch(self, request: HttpRequest, pk):
        return self.update_event_category(request, pk)

    def update_event_category(self, request: HttpRequest, pk):
        serializer = self.InputEventCategorySerializer(
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        category = event_category_get(pk)
        try:
            updated_category = event_category_update(
                category=category, data=serializer.validated_data)
            return Response(EventCategoryDetailApi.OutputEventCategorySerializer(updated_category).data, status=status.HTTP_200_OK)
        except Exception as e:
            if e.get_codes() == ['no_content']:
                return Response({'detail': 'No changes detected. event category data remains the same.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class EventCategoryGetwayApiViewSet(ViewSet):
    def list(self, request: HttpRequest):
        return EventCategoryListApi.as_view()(request._request)

    def retrieve(self, request: HttpRequest, pk=None):
        return EventCategoryDetailApi.as_view()(request._request, pk=pk)

    def create(self, request: HttpRequest):
        return EventCategoryCreateApi.as_view()(request._request)

    def update(self, request: HttpRequest, pk=None):
        return EventCategoryUpdateApi.as_view()(request._request, pk=pk)

    def partial_update(self, request: HttpRequest, pk=None):
        return EventCategoryUpdateApi.as_view()(request._request, pk=pk)
