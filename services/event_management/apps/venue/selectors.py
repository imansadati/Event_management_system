from .models import Venue
from .filters import VenueFilter


def venue_list(*, filters):
    filters = filters or {}

    qs = Venue.objects.all()
    return VenueFilter(filters, qs).qs
