from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from .models import Speaker
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework import serializers
from .selectors import speaker_list, speaker_get
from rest_framework import status
from rest_framework.response import Response
from .services import speaker_create


class SpeakerListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputSpeakerListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Speaker
            fields = '__all__'

    class FilterSpeakerSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=128, required=False)
        type = serializers.CharField(max_length=100, required=False)
        status = serializers.CharField(max_length=100, required=False)

    def get(self, request: HttpRequest):
        filter_serializers = self.FilterSpeakerSerializer(
            data=request.query_params)
        filter_serializers.is_valid(raise_exception=True)

        speakers = speaker_list(filters=filter_serializers.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSpeakerListSerializer,
            queryset=speakers,
            request=request,
            view=self
        )


class SpeakerDetailApi(APIView):
    class OutputSpeakerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Speaker
            exclude = ['created_at', 'updated_at']

    def get(self, request: HttpRequest, pk):
        speaker = speaker_get(pk)

        data = self.OutputSpeakerSerializer(speaker).data

        return Response(data, status=status.HTTP_200_OK)


class SpeakerCreateApi(APIView):
    class InputSpeakerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Speaker
            exclude = ['created_at', 'updated_at']

    def post(self, reqeust: HttpRequest):
        serializer = self.InputSpeakerSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)

        speaker = speaker_create(**serializer.validated_data)

        data = SpeakerDetailApi.OutputSpeakerSerializer(speaker).data
        return Response(data, status=status.HTTP_201_CREATED)


# To make endpoints RestFull
class SpeakerGetwayApiViewset(ViewSet):
    def list(self, request: HttpRequest):
        return SpeakerListApi.as_view()(request._request)

    def retrieve(self, request: HttpRequest, pk=None):
        return SpeakerDetailApi.as_view()(request._request, pk=pk)

    def create(self, request: HttpRequest):
        return SpeakerCreateApi.as_view()(request._request)
