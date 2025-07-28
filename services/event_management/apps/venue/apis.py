from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework import serializers
from .models import Venue
from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from .selectors import venue_list, venue_get
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import venue_create, venue_update
from rest_framework import status
from rest_framework.exceptions import ValidationError


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


class VenueDetailApi(APIView):
    class OutputVenueSerializer(serializers.ModelSerializer):
        class Meta:
            model = Venue
            exclude = ['created_at', 'updated_at']

    def get(self, request: HttpRequest, pk):
        venue = venue_get(pk)

        data = self.OutputVenueSerializer(venue).data

        return Response(data, status=status.HTTP_200_OK)


class VenueCreateApi(APIView):
    class InputVenueSerializer(serializers.ModelSerializer):
        class Meta:
            model = Venue
            exclude = ['created_at', 'updated_at']
            extra_kwargs = {'venue_type': {'required': True}}

    def post(self, reqeust: HttpRequest):
        serializer = self.InputVenueSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)

        venue = venue_create(**serializer.validated_data)

        data = VenueDetailApi.OutputVenueSerializer(venue).data
        return Response(data, status=status.HTTP_201_CREATED)


class VenueUpdateApi(APIView):
    class InputVenueSerializer(serializers.ModelSerializer):
        class Meta:
            model = Venue
            fields = ['name', 'address', 'city',
                      'capacity']  # add more if needed

        # check the user does not enter additional fields
        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def put(self, request: HttpRequest, pk):
        return self.update_venue(request, pk)

    def patch(self, request: HttpRequest, pk):
        return self.update_venue(request, pk)

    def update_venue(self, request: HttpRequest, pk):
        serializer = self.InputVenueSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        venue = venue_get(pk)
        try:
            updated_venue = venue_update(
                venue=venue, data=serializer.validated_data)
            return Response(VenueDetailApi.OutputVenueSerializer(updated_venue).data, status=status.HTTP_200_OK)
        except Exception as e:
            if e.get_codes() == ['no_content']:
                return Response({'detail': 'No changes detected. venue data remains the same.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class VenueDeleteApi(APIView):
    def delete(self, reqeust: HttpRequest, pk):
        venue = venue_get(pk)

        venue.delete()

        return Response({'detail': f'This venue with {pk} id successfully deleted.'}, status=status.HTTP_200_OK)


class VenueGetwayApiViewset(ViewSet):
    def list(self, request: HttpRequest):
        return VenueListApi.as_view()(request._request)

    def retrieve(self, request: HttpRequest, pk=None):
        return VenueDetailApi.as_view()(request._request, pk=pk)

    def create(self, request: HttpRequest):
        return VenueCreateApi.as_view()(request._request)

    def update(self, request: HttpRequest, pk=None):
        return VenueUpdateApi.as_view()(request._request, pk=pk)

    def partial_update(self, request: HttpRequest, pk=None):
        return VenueUpdateApi.as_view()(request._request, pk=pk)

    def delete(self, request: HttpRequest, pk=None):
        return VenueDeleteApi.as_view()(request._request, pk=pk)
