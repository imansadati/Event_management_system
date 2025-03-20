from apps.users.models import AttendeeUser, AdminUser, StaffUser
from django.db.models import Q


def get_attendee_by_identifier(identifier):
    """Fetch a user using email or username"""
    user = (
        AttendeeUser.objects.filter(Q(email=identifier) | Q(username=identifier)).first() or
        AdminUser.objects.filter(Q(email=identifier) | Q(username=identifier)).first() or
        StaffUser.objects.filter(Q(email=identifier) | Q(username=identifier)).first()
    )
    return user

    
