from .models import Venue
from .filters import VenueFilter
from django.shortcuts import get_object_or_404


def venue_list(*, filters):
    filters = filters or {}

    qs = Venue.objects.all()
    return VenueFilter(filters, qs).qs


def venue_get(venue_id):
    return get_object_or_404(Venue, id=venue_id)
