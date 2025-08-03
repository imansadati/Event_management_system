from django.db import transaction
from .models import Session
from .selectors import session_time_conflict
from rest_framework.exceptions import ValidationError
from shared_utils.update_model import model_update


def session_update(*, session: Session, data):
    non_side_effect_fields = [
        'title',
        'capacity'
    ]

    try:
        updated_session = model_update(
            instance=session, fields=non_side_effect_fields, data=data
        )
        return updated_session
    except ValidationError as e:
        raise e


@transaction.atomic()
def session_create(event, **kwargs):
    # * TODO: must assign session speaker
    start = kwargs.get('start_datetime')
    end = kwargs.get('end_datetime')
    venue = kwargs.get('venue')

    time_conflict = session_time_conflict(event, start, end)

    if time_conflict:
        raise ValidationError(
            'start_Session time conflicts with an existing time.')

    session_data = {
        'event': event,
        'start_datetime': start,
        'end_datetime': end,
        'title': kwargs.get('title'),
        'description': kwargs.get('description'),
        'capacity': kwargs.get('capacity'),
    }

    if venue:
        session_data['venue'] = venue

    return Session.objects.create(**session_data)
