from rest_framework.views import APIView
from rest_framework import serializers
from .models import Organizer, OrganizerMember
from django.http import HttpRequest
from rest_framework.response import Response
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from .selectors import organizer_list, organizer_get
from rest_framework.viewsets import ViewSet
from rest_framework import status
from .services import organizer_create, organizer_update
from rest_framework.exceptions import ValidationError


# organizer CRUD
class OrganizerListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputOrganizerListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organizer
            fields = '__all__'

    class FilterOrganizerSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=128, required=False)
        type = serializers.CharField(max_length=16, required=False)

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


class OrganizerDetailApi(APIView):
    class OutputOrganizerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organizer
            exclude = ['created_at', 'updated_at']

    def get(self, request: HttpRequest, pk):
        organizer = organizer_get(pk)

        data = self.OutputOrganizerSerializer(organizer).data

        return Response(data, status=status.HTTP_200_OK)


class OrganizerCreateApi(APIView):
    class InputOrganizerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organizer
            exclude = ['created_at', 'updated_at']
            extra_kwargs = {'description': {'required': True}}
            extra_kwargs = {'type': {'required': True}}

    def post(self, reqeust: HttpRequest):
        serializer = self.InputOrganizerSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)

        organizer = organizer_create(**serializer.validated_data)

        data = OrganizerDetailApi.OutputOrganizerSerializer(organizer).data
        return Response(data, status=status.HTTP_201_CREATED)


class OrganizerUpdateApi(APIView):
    class InputOrganizerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organizer
            fields = ['name', 'website']  # add more if needed

        # check the user does not enter additional fields
        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def put(self, request: HttpRequest, pk):
        return self.update_organizer(request, pk)

    def patch(self, request: HttpRequest, pk):
        return self.update_organizer(request, pk)

    def update_organizer(self, request: HttpRequest, pk):
        serializer = self.InputOrganizerSerializer(
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        organizer = organizer_get(pk)
        try:
            updated_organizer = organizer_update(
                organizer=organizer, data=serializer.validated_data)
            return Response(OrganizerDetailApi.OutputOrganizerSerializer(updated_organizer).data, status=status.HTTP_200_OK)
        except Exception as e:
            if e.get_codes() == ['no_content']:
                return Response({'detail': 'No changes detected. organizer data remains the same.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class OrganizerDeleteApi(APIView):
    def delete(self, reqeust: HttpRequest, pk):
        organizer = organizer_get(pk)

        organizer.delete()

        return Response({'detail': f'This organizer with {pk} id successfully deleted.'}, status=status.HTTP_200_OK)


class OrganizerGetwayApiViewset(ViewSet):
    def list(self, request: HttpRequest):
        return OrganizerListApi.as_view()(request._request)

    def retrieve(self, request: HttpRequest, pk=None):
        return OrganizerDetailApi.as_view()(request._request, pk=pk)

    def create(self, request: HttpRequest):
        return OrganizerCreateApi.as_view()(request._request)

    def update(self, request: HttpRequest, pk=None):
        return OrganizerUpdateApi.as_view()(request._request, pk=pk)

    def partial_update(self, request: HttpRequest, pk=None):
        return OrganizerUpdateApi.as_view()(request._request, pk=pk)

    def delete(self, request: HttpRequest, pk=None):
        return OrganizerDeleteApi.as_view()(request._request, pk=pk)
