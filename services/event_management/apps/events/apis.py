from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpRequest
from .models import Event
from rest_framework.response import Response
from .selectors import event_list


class EventListApi(APIView):
    class OutputEventListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = '__all__'

    def get(self, request: HttpRequest):
        data = event_list()
        serializer = self.OutputEventListSerializer(data, many=True).data
        return Response(serializer)
