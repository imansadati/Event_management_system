import django_filters
from .models import Organizer


class OrganizerFilter(django_filters.FilterSet):
    class Meta:
        model = Organizer
        fields = {
            'name': ['exact'],
            'type': ['exact'],
        }
