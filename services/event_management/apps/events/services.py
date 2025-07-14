from .models import Event
from django.db import transaction
from django.utils import timezone
from .tasks import publsih_event_task
from shared_utils.update_model import model_update
from rest_framework.exceptions import ValidationError


@transaction.atomic()
def event_create(**kwargs):
    now = timezone.now()

    published_at = kwargs['published_at']

    event = Event.objects.create_event(**kwargs)

    if published_at:
        if published_at >= now:
            kwargs['status'] = 'archived'  # keep archived until publish timet
            # scheduled a background task to publish event
            publsih_event_task.apply_async(
                args=[event.id], eta=published_at, priority=4)

        else:
            kwargs['status'] = 'published'

    return event


def event_update(*, event: Event, data):
    non_side_effect_fields = [
        'title',
        'capacity'
    ]

    try:
        updated_event = model_update(
            instance=event, fields=non_side_effect_fields, data=data
        )
        return updated_event
    except ValidationError as e:
        raise e
