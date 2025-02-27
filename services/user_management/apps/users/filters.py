import django_filters
from .models import AdminUser


class AdminFilter(django_filters.FilterSet):
    class Meta:
        model = AdminUser
        fields = {
            'email': ['exact'],
            'username': ['exact'],
            'full_name': ['iexact'],
            'is_admin': ['exact'],
        }
