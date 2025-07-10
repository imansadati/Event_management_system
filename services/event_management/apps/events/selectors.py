from .models import Event


def event_list():
    return Event.objects.all()
