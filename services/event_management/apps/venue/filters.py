from django_filters.filterset import FilterSet
from .models import Venue


class VenueFilter(FilterSet):
    class Meta:
        model = Venue
        fields = {
            'name': ['exact'],
            'city': ['exact'],
        }
