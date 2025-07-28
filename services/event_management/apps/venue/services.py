from django.db import transaction
from .models import Venue
from shared_utils.update_model import model_update
from rest_framework.exceptions import ValidationError


@transaction.atomic()
def venue_create(**kwargs):
    venue = Venue.objects.create(**kwargs)

    return venue


def venue_update(*, venue: Venue, data):
    non_side_effect_fields = [
        'name',
        'address',
        'city',
        'capacity'
    ]

    try:
        updated_venue = model_update(
            instance=venue, fields=non_side_effect_fields, data=data
        )
        return updated_venue
    except ValidationError as e:
        raise e
