from apps.users.models import AttendeeUser, AdminUser, StaffUser
from django.db.models import Q


def get_user_by_identifier(identifier):
    """Fetch a user using email or username and check roles."""
    user = (
        AttendeeUser.objects.filter(Q(email=identifier) | Q(username=identifier) & Q(is_attendee=True)).first() or
        AdminUser.objects.filter(Q(email=identifier) | Q(username=identifier) & Q(is_admin=True)).first() or
        StaffUser.objects.filter(Q(email=identifier) | Q(
            username=identifier) & Q(is_staff=True)).first()
    )
    return user


def get_user_by_id(user_id):
    """Fetch a user using id and check roles."""
    user = (
        AttendeeUser.objects.filter(Q(id=user_id) & Q(is_attendee=True)).first() or
        AdminUser.objects.filter(Q(id=user_id) & Q(is_admin=True)).first() or
        StaffUser.objects.filter(Q(id=user_id) & Q(is_staff=True)).first()
    )
    return user


def get_user_by_email(email):
    """Fetch a user using email and check roles."""
    user = (
        AttendeeUser.objects.filter(Q(email=email) & Q(is_attendee=True)).first() or
        AdminUser.objects.filter(Q(email=email) & Q(is_admin=True)).first() or
        StaffUser.objects.filter(Q(email=email) & Q(is_staff=True)).first()
    )
    return user


def get_user_by_email_and_id(id, email):
    """Fetch a user using email and id also check roles."""
    user = (
        AttendeeUser.objects.filter(Q(email=email) & Q(is_attendee=True)).first() or
        AdminUser.objects.filter(Q(email=email) & Q(is_admin=True)).first() or
        StaffUser.objects.filter(Q(email=email) & Q(is_staff=True)).first()
    )
    return user
