from .models import Speaker
from django.db import transaction


@transaction.atomic()
def speaker_create(**kwargs):
    speaker = Speaker.objects.create(**kwargs)

    return speaker
