from .models import Speaker
from django.db import transaction
from shared_utils.update_model import model_update
from rest_framework.exceptions import ValidationError


@transaction.atomic()
def speaker_create(**kwargs):
    speaker = Speaker.objects.create(**kwargs)

    return speaker


def speaker_update(*, speaker: Speaker, data):
    non_side_effect_fields = [
        'name',
        'bio',
        'status',
    ]

    try:
        updated_speaker = model_update(
            instance=speaker, fields=non_side_effect_fields, data=data
        )
        return updated_speaker
    except ValidationError as e:
        raise e
