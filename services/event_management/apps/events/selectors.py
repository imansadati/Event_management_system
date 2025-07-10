from .models import Event
from .filters import EventFilter


def event_list(*, filters):
    filters = filters or {}

    qs = Event.objects.all()
    return EventFilter(filters, qs).qs
