from django_filters.filterset import FilterSet
from .models import Speaker


class SpeakerFilter(FilterSet):
    class Meta:
        model = Speaker
        fields = {
            'name': ['exact'],
            'status': ['exact'],
            'type': ['exact'],
        }
