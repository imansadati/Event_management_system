from .models import Session
from django.db.models import Q
from .models import Session
from .filters import SessionFilter


def session_time_conflict(event, start_time, end_time):
    return Session.objects.filter(
        Q(start_datetime__lt=end_time) & Q(end_datetime__gt=start_time),
        event=event
    ).exists()


def session_list(*, filters):
    filters = filters or {}

    qs = Session.objects.all()
    return SessionFilter(filters, qs).qs
