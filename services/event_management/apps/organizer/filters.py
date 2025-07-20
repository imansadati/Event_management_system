import django_filters
from .models import Organizer, OrganizerMember


class OrganizerFilter(django_filters.FilterSet):
    class Meta:
        model = Organizer
        fields = {
            'name': ['exact'],
            'type': ['exact'],
        }


class OrganizerMemberFilter(django_filters.FilterSet):
    class Meta:
        model = OrganizerMember
        fields = {
            'role': ['exact'],
        }
