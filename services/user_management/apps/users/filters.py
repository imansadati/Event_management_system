import django_filters
from .models import AdminUser, StaffUser


class AdminFilter(django_filters.FilterSet):
    class Meta:
        model = AdminUser
        fields = {
            'email': ['exact'],
            'username': ['exact'],
            'full_name': ['iexact'],
            'is_admin': ['exact'],
        }


class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = StaffUser
        fields = {
            'email': ['iexact'],
            'job_title': ['exact'],
            'availability_status': ['exact'],
            'username': ['exact'],
            'full_name': ['iexact'],
            'is_staff': ['exact'],
        }
