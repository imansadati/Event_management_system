from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from .models import Speaker
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework import serializers
from .selectors import speaker_list, speaker_get
from rest_framework import status
from rest_framework.response import Response
from .services import speaker_create, speaker_update
from rest_framework.exceptions import ValidationError


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


class SpeakerUpdateApi(APIView):
    class InputSpeakerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Speaker
            fields = ['name', 'bio', 'status']  # add more if needed

        # check the user does not enter additional fields
        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def put(self, request: HttpRequest, pk):
        return self.update_speaker(request, pk)

    def patch(self, request: HttpRequest, pk):
        return self.update_speaker(request, pk)

    def update_speaker(self, request: HttpRequest, pk):
        serializer = self.InputSpeakerSerializer(
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        speaker = speaker_get(pk)
        try:
            updated_speaker = speaker_update(
                speaker=speaker, data=serializer.validated_data)
            return Response(SpeakerDetailApi.OutputSpeakerSerializer(updated_speaker).data, status=status.HTTP_200_OK)
        except Exception as e:
            if e.get_codes() == ['no_content']:
                return Response({'detail': 'No changes detected. Speaker data remains the same.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class SpeakerDeleteApi(APIView):
    def delete(self, reqeust: HttpRequest, pk):
        speaker = speaker_get(pk)

        speaker.delete()

        return Response({'detail': f'This speaker with {pk} id successfully deleted.'}, status=status.HTTP_200_OK)


# To make endpoints RestFull
class SpeakerGetwayApiViewset(ViewSet):
    def list(self, request: HttpRequest):
        return SpeakerListApi.as_view()(request._request)

    def retrieve(self, request: HttpRequest, pk=None):
        return SpeakerDetailApi.as_view()(request._request, pk=pk)

    def create(self, request: HttpRequest):
        return SpeakerCreateApi.as_view()(request._request)

    def update(self, request: HttpRequest, pk=None):
        return SpeakerUpdateApi.as_view()(request._request, pk=pk)

    def partial_update(self, request: HttpRequest, pk=None):
        return SpeakerUpdateApi.as_view()(request._request, pk=pk)

    def delete(self, request: HttpRequest, pk=None):
        return SpeakerDeleteApi.as_view()(request._request, pk=pk)
