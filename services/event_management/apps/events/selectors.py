from .models import Event
from .filters import EventFilter
from django.shortcuts import get_object_or_404


def event_list(*, filters):
    filters = filters or {}

    qs = Event.objects.filter(status='published')
    return EventFilter(filters, qs).qs


def event_get(event_id):
    return get_object_or_404(Event, id=event_id)
