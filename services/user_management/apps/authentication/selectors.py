from apps.users.models import AttendeeUser, AdminUser, StaffUser
from django.db.models import Q


ROLE_MODEL_MAP = {
    'attendee': AttendeeUser,
    'admin': AdminUser,
    'staff': StaffUser,
}


def get_user_by_identifier(identifier):
    """Fetch a user using email or username and check roles."""
    user = (
        AttendeeUser.objects.filter(Q(email=identifier) | Q(username=identifier) & Q(is_attendee=True)).first() or
        AdminUser.objects.filter(Q(email=identifier) | Q(username=identifier) & Q(is_admin=True)).first() or
        StaffUser.objects.filter(Q(email=identifier) | Q(
            username=identifier) & Q(is_staff=True)).first()
    )
    return user


def get_user_by_id(user_id, role):
    """Fetch a user using id and check roles."""
    model = ROLE_MODEL_MAP.get(role)
    status = f'is_{role}'

    if not model:
        return None

    return model.objects.filter(id=user_id, **{status: True}).first()


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
        AttendeeUser.objects.filter(Q(email=email) & Q(id=id) & Q(is_attendee=True)).first() or
        AdminUser.objects.filter(Q(email=email) & Q(id=id) & Q(is_admin=True)).first() or
        StaffUser.objects.filter(Q(email=email) & Q(
            id=id) & Q(is_staff=True)).first()
    )
    return user
