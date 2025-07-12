from .models import Event
from django.db import transaction
from django.utils import timezone
from .tasks import publsih_event_task


@transaction.atomic()
def event_create(**kwargs):
    now = timezone.now()

    published_at = kwargs['published_at']

    event = Event.objects.create_event(**kwargs)

    if published_at:
        if published_at > now:
            kwargs['status'] = 'archived'  # keep archived until publish timet
            # scheduled a background task to publish event
            publsih_event_task.apply_async(
                args=[event.id], eta=published_at, priority=4)

        else:
            kwargs['status'] = 'published'

    return event
