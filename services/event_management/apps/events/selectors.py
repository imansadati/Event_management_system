from .models import Event, EventCategory
from .filters import EventFilter, EventCategoryFilter
from django.shortcuts import get_object_or_404


def event_list(*, filters):
    filters = filters or {}

    qs = Event.objects.filter(status='published')
    return EventFilter(filters, qs).qs


def event_get(event_id):
    return get_object_or_404(Event, id=event_id)


def event_category_list(*, filters):
    filters = filters or {}

    qs = EventCategory.objects.filter(is_active=True)
    return EventCategoryFilter(filters, qs).qs


def event_category_get(category_id):
    return get_object_or_404(EventCategory, id=category_id)
