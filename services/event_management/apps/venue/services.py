from django.db import transaction
from .models import Venue


@transaction.atomic()
def venue_create(**kwargs):
    venue = Venue.objects.create(**kwargs)

    return venue
