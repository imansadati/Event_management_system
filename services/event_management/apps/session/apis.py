from rest_framework.views import APIView
from rest_framework import serializers, status
from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from .models import Session
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from apps.events.selectors import event_get
from .services import session_create, session_update
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from .selectors import session_list, session_get
from apps.events.apis import EventDetailApi


# add permission to check only organizer/admins can access to this api
class SessionDetailApi(APIView):
    class OutputSessionSerializer(serializers.ModelSerializer):
        event = EventDetailApi.OutputEventSerializer()

        class Meta:
            model = Session
            exclude = ['created_at', 'updated_at']

    def get(self, request: HttpRequest, session_id=None):
        session = session_get(session_id)

        data = self.OutputSessionSerializer(session).data

        return Response(data, status=status.HTTP_200_OK)


class SessionUpdateApi(APIView):
    class InputSessionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Session
            fields = ['title', 'capacity']  # add more if needed

        # check the user does not enter additional fields
        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def put(self, request: HttpRequest, session_id):
        return self.update_session(request, session_id)

    def patch(self, request: HttpRequest, session_id):
        return self.update_session(request, session_id)

    def update_session(self, request: HttpRequest, session_id=None):
        serializer = self.InputSessionSerializer(
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        session = session_get(session_id)
        try:
            updated_session = session_update(
                session=session, data=serializer.validated_data)
            return Response(SessionDetailApi.OutputSessionSerializer(updated_session).data, status=status.HTTP_200_OK)
        except Exception as e:
            if e.get_codes() == ['no_content']:
                return Response({'detail': 'No changes detected. session data remains the same.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class SessionEventCreateApi(APIView):
    class InputSessionEventSerializer(serializers.ModelSerializer):
        class Meta:
            model = Session
            exclude = ['status', 'created_at', 'updated_at', 'event']
            extra_kwargs = {'capacity': {'required': True}}

        def validate(self, data):
            if data['start_datetime'] >= data['end_datetime']:
                raise ValidationError(
                    {'start_datetime': 'start_datetime must be before end_datetime'}
                )
            return data

    def post(self, request: HttpRequest, event_id=None):
        serializer = self.InputSessionEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_start_datetime = serializer.validated_data.get(
            'start_datetime')
        session_end_datetime = serializer.validated_data.get('end_datetime')

        event = event_get(event_id)

        if session_start_datetime < event.start_datetime or session_end_datetime > event.end_datetime:
            raise ValidationError(
                detail='The Session datetime conflict with the event datetime.')

        try:
            session = session_create(event=event, **serializer.validated_data)
            return Response(SessionDetailApi.OutputSessionSerializer(session).data, status=status.HTTP_200_OK)
        except Exception as e:
            if e.get_codes() == ['no_content']:
                return Response({'detail': 'No changes detected. session data remains the same.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class SessionEventListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputSessionEventListSerializer(serializers.ModelSerializer):
        event = EventDetailApi.OutputEventSerializer()

        class Meta:
            model = Session
            fields = '__all__'

    class FilterSessionEventSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=128, required=False)
        event = serializers.IntegerField(required=False)

    def get(self, request: HttpRequest, event_id=None):
        filter_serializers = self.FilterSessionEventSerializer(
            data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)

        event = event_get(event_id)

        sessions = session_list(
            filters=filter_serializers.validated_data, event=event)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSessionEventListSerializer,
            queryset=sessions,
            request=request,
            view=self
        )


class SessionEventGetwayApiViewSet(ViewSet):
    def create(self, request: HttpRequest, event_id=None):
        return SessionEventCreateApi.as_view()(request._request, event_id=event_id)

    def list(self, request: HttpRequest, event_id=None):
        return SessionEventListApi.as_view()(request._request, event_id=event_id)


class SessionGetwayApiViewSet(ViewSet):
    def retrieve(self, request: HttpRequest, session_id=None):
        return SessionDetailApi.as_view()(request._request, session_id=session_id)

    def update(self, request: HttpRequest, session_id=None):
        return SessionUpdateApi.as_view()(request._request, session_id=session_id)

    def partial_update(self, request: HttpRequest, session_id=None):
        return SessionUpdateApi.as_view()(request._request, session_id=session_id)
