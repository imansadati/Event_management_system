from .models import Speaker
from .filters import SpeakerFilter


def speaker_list(*, filters):
    filters = filters or {}

    qs = Speaker.objects.all()
    return SpeakerFilter(filters, qs).qs
