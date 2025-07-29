from .models import Speaker
from .filters import SpeakerFilter
from django.shortcuts import get_object_or_404


def speaker_list(*, filters):
    filters = filters or {}

    qs = Speaker.objects.all()
    return SpeakerFilter(filters, qs).qs


def speaker_get(speaker_id):
    return get_object_or_404(Speaker, id=speaker_id)
