from .models import Organizer
from django.db import transaction


@transaction.atomic()
def organizer_create(**kwargs):
    organizer = Organizer.objects.create(**kwargs)

    return organizer
