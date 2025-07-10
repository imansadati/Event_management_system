from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpRequest
from .models import Event
from .selectors import event_list
from shared_utils.pagination import get_paginated_response, LimitOffsetPagination


class EventListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class OutputEventListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = '__all__'

    def get(self, request: HttpRequest):
        events = event_list()

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputEventListSerializer,
            queryset=events,
            request=request,
            view=self
        )


class EventGetwayApiViewSet(ViewSet):
    def list(self, request):
        return EventListApi.as_view()(request._request)
