from .models import Event
from django.db import transaction
from django.utils import timezone


@transaction.atomic()
def event_create(**kwargs):
    print(kwargs)
    now = timezone.now()

    print('1223333333333333333333')
    published_at = kwargs['published_at']

    if published_at:
        if published_at > now:
            kwargs['status'] = 'archived'
            # keep archived until publish timet
            # schedule a background task (Celery etc.)

        else:
            kwargs['status'] = 'published'

    event = Event.objects.create_event(**kwargs)
    print('ehsan sadatiiiiiiiiiiiiiiiiiiiii')
    return event
