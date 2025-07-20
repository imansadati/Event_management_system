from .models import Organizer
from .filters import OrganizerFilter
from django.shortcuts import get_object_or_404


def organizer_list(*, filters):
    filters = filters or {}

    qs = Organizer.objects.all()
    return OrganizerFilter(filters, qs).qs


def organizer_get(organizer_id):
    return get_object_or_404(Organizer, id=organizer_id)
