from .models import Event, EventCategory, EventGuest
from .filters import EventFilter, EventCategoryFilter, EventGuestFilter
from django.shortcuts import get_object_or_404
from django.utils import timezone


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


def guest_get_by_email(email) -> bool:
    return EventGuest.objects.filter(email=email).exists()


def guest_get_by_id_and_event(guest_id, event):
    return get_object_or_404(EventGuest, id=guest_id, event=event)


def event_guest_list(*, filters, event_id):
    filters = filters or {}

    qs = EventGuest.objects.filter(
        event__status='published', event__id=event_id, event__end_datetime__gte=timezone.now())
    return EventGuestFilter(filters, qs).qs
