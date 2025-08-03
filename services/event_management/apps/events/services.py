from .models import EventGuest, EventInvite
from .models import Event, EventCategory
from django.db import transaction
from django.utils import timezone
from .tasks import publsih_event_task
from shared_utils.update_model import model_update
from rest_framework.exceptions import ValidationError
from django.utils import timezone


# * TODO: Must assign event speaker
@transaction.atomic()
def event_create(**kwargs):
    now = timezone.now()

    published_at = kwargs['published_at']

    event = Event.objects.create_event(**kwargs)

    if published_at:
        if published_at >= now:
            event.status = 'archived'  # keep archived until publish time
            event.save(update_fields=['status'])
            # scheduled a background task to publish event
            publsih_event_task.apply_async(
                args=[event.id], eta=published_at, priority=4)

        else:
            event.status = 'published'
            event.published_at = now
            event.save(update_fields=['status', 'published_at'])

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


@transaction.atomic()
def event_category_create(**kwargs):
    category = EventCategory(
        **kwargs
    )
    category.is_active = True
    category.full_clean()
    category.save()

    return category


def event_category_update(*, category: EventCategory, data):
    non_side_effect_fields = [
        'title',
    ]

    try:
        updated_category = model_update(
            instance=category, fields=non_side_effect_fields, data=data
        )
        return updated_category
    except ValidationError as e:
        raise e


@transaction.atomic()
def guest_create(email, current_user, event):
    return EventGuest.objects.get_or_create(
        event=event, email=email, defaults={'user_invited_by': current_user})


@transaction.atomic()
def invite_create(email, event, current_user, default_exp):
    now = timezone.now()
    return EventInvite.objects.get_or_create(
        email=email, event=event, defaults={'user_invited_by': current_user, 'expires_at': now + timezone.timedelta(hours=default_exp)})
