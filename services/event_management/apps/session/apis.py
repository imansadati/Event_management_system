from rest_framework.views import APIView
from rest_framework import serializers, status
from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from .models import Session
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from apps.events.selectors import event_get
from .services import session_create


# events/event_id/sessions/  Create

# events/event_id/sessions/  List
# sessions/session_id  retrieve
# sessions/session_id  update & partial update


# add permission to check only organizer/admins can access to this api
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

        session = session_create(event=event, **serializer.validated_data)

        return Response(data='test', status=status.HTTP_201_CREATED)


class SessionEventGetwayApiViewSet(ViewSet):
    def create(self, request: HttpRequest, event_id=None):
        return SessionEventCreateApi.as_view()(request._request, event_id=event_id)
