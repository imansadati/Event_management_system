from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpRequest
from .models import Event, EventCategory
from .selectors import (event_list, event_get, event_category_list, event_category_get,
                        event_guest_list, guest_get_by_id_and_event, event_invite_list)
from .services import (event_create, event_update, event_category_create,
                       event_category_update, guest_create, invite_create,
                       set_organizer_member)
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from apps.events.models import EventGuest, EventInvite
from grpc_service.client.client import send_email_via_rpc
from apps.organizer.apis import OrganizerListApi


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


class EventCategoryDeleteApi(APIView):
    def delete(self, reqeust: HttpRequest, pk):
        category = event_category_get(pk)

        category.delete()

        return Response({'detail': f'This event category with {pk} id successfully deleted.'}, status=status.HTTP_200_OK)


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

    def delete(self, request: HttpRequest, pk=None):
        return EventCategoryDeleteApi.as_view()(request._request, pk=pk)


class EventListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputEventListSerializer(serializers.ModelSerializer):
        organizer = OrganizerListApi.OutputOrganizerListSerializer(
            read_only=True)
        category = EventCategoryListApi.OutputEventCategoryListSerializer(
            read_only=True)

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
        organizer = OrganizerListApi.OutputOrganizerListSerializer(
            read_only=True)
        category = EventCategoryListApi.OutputEventCategoryListSerializer(
            read_only=True)

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
            return data

    def post(self, reqeust: HttpRequest):
        serializer = self.InputEventSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)

        event = event_create(**serializer.validated_data)

        set_organizer_member(event, reqeust.user.id)

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


# Those emails in guest list can see private events.
# Test this api when added permissions
class EventGuestCreateApi(APIView):
    class InputEventGuestSerializer(serializers.ModelSerializer):
        class Meta:
            model = EventGuest
            fields = ['email']

    def post(self, request: HttpRequest, event_id=None):
        serializer = self.InputEventGuestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = 1  # test
        email = serializer.validated_data.get('email')

        event = event_get(event_id)

        if event.type != 'private':
            return Response({'detail': 'Guest list is only for private events.'}, status=status.HTTP_409_CONFLICT)

        guest, created = guest_create(
            email=email, current_user=current_user, event=event)

        return Response(data={'detail': f'This {guest.email} email successfully added in guest list.'}, status=status.HTTP_201_CREATED)


class EventGuestListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputEventGuestListSerializer(serializers.ModelSerializer):
        class Meta:
            model = EventGuest
            fields = '__all__'

    class FilterEventGuestSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)

    def get(self, request: HttpRequest, event_id=None):
        filter_serializers = self.FilterEventGuestSerializer(
            data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)

        event = event_get(event_id)

        if event.type != 'private':
            return Response({'detail': 'Guest list is only for private events.'}, status=status.HTTP_409_CONFLICT)

        guests = event_guest_list(
            filters=filter_serializers.validated_data, event_id=event_id)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputEventGuestListSerializer,
            queryset=guests,
            request=request,
            view=self
        )


class EventGuestDeleteApi(APIView):
    def delete(self, reqeust: HttpRequest, event_id=None, guest_id=None):
        event = event_get(event_id)

        if event.type != 'private':
            return Response({'detail': 'Guest list is only for private events.'}, status=status.HTTP_409_CONFLICT)

        guest = guest_get_by_id_and_event(guest_id=guest_id, event=event)
        guest.delete()

        return Response({'detail': f'This guest with {guest_id} id successfully deleted.'}, status=status.HTTP_200_OK)


class EventGuestGetwayApiViewSet(ViewSet):
    def create(self, request: HttpRequest, event_id=None):
        return EventGuestCreateApi.as_view()(request._request, event_id=event_id)

    def list(self, request: HttpRequest, event_id=None):
        return EventGuestListApi.as_view()(request._request, event_id=event_id)

    def delete(self, request: HttpRequest, event_id=None, guest_id=None):
        return EventGuestDeleteApi.as_view()(request._request, event_id=event_id, guest_id=guest_id)


# Test this api when added permissions
class EventInviteCreateApi(APIView):
    class InputEventInviteSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)
        expires_in_hours = serializers.IntegerField(required=False)

    def post(self, request: HttpRequest, event_id=None):
        serializer = self.InputEventInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = 1

        event = event_get(event_id)

        if event.type != 'invite_only':
            return Response({'detail': 'Invites are only for invite_only events.'}, status=status.HTTP_409_CONFLICT)

        default_exp = serializer.validated_data.get('expires_in_hours', 48)
        email = serializer.validated_data.get('email')

        invite, created = invite_create(
            email=email, event=event, current_user=current_user, default_exp=default_exp)

        if created:
            # * TODO: Must complete this section after finished session apis.
            invite_url = 'test'
            send_email_via_rpc(invite.email, 'Invited to the event',
                               f'Click on this link to sign-up {invite_url}')

        return Response(data={'detail': f'This {invite.email} email successfully sent invite for it.'}, status=status.HTTP_201_CREATED)


class EventInviteListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputEventInviteListSerializer(serializers.ModelSerializer):
        class Meta:
            model = EventInvite
            fields = '__all__'

    class FilterEventInviteSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)

    def get(self, request: HttpRequest, event_id=None):
        filter_serializers = self.FilterEventInviteSerializer(
            data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)

        event = event_get(event_id)

        if event.type != 'invite_only':
            return Response({'detail': 'Invites are only for invite_only events.'}, status=status.HTTP_409_CONFLICT)

        invites = event_invite_list(
            filters=filter_serializers.validated_data, event_id=event_id)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputEventInviteListSerializer,
            queryset=invites,
            request=request,
            view=self
        )


class EventInviteGetwayApiViewSet(ViewSet):
    def create(self, request: HttpRequest, event_id=None):
        return EventInviteCreateApi.as_view()(request._request, event_id=event_id)

    def list(self, request: HttpRequest, event_id=None):
        return EventInviteListApi.as_view()(request._request, event_id=event_id)
