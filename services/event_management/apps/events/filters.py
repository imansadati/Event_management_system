import django_filters
from .models import Event, EventCategory


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'title': ['exact'],
            'type': ['exact'],
        }


class EventCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = EventCategory
        fields = {
            'title': ['exact'],
        }
