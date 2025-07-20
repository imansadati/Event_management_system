from .models import Organizer
from .filters import OrganizerFilter


def organizer_list(*, filters):
    filters = filters or {}

    qs = Organizer.objects.all()
    return OrganizerFilter(filters, qs).qs
