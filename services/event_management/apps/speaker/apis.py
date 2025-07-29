from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework.viewsets import ViewSet
from .models import Speaker
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework import serializers
from .selectors import speaker_list


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


# To make endpoints RestFull
class SpeakerGetwayApiViewset(ViewSet):
    def list(self, request: HttpRequest):
        return SpeakerListApi.as_view()(request._request)
