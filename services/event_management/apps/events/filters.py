import django_filters
from .models import Event, EventCategory, EventGuest, EventInvite


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


class EventGuestFilter(django_filters.FilterSet):
    class Meta:
        model = EventGuest
        fields = {
            'email': ['exact'],
        }


class EventInviteFilter(django_filters.FilterSet):
    class Meta:
        model = EventInvite
        fields = {
            'email': ['exact'],
        }
