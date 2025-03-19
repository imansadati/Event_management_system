from apps.users.models import AttendeeUser


def get_attendee_by_identifier(identifier):
    """Fetch a user using email or username"""
    if '@' in identifier:
        return AttendeeUser.objects.filter(email=identifier).first()
    return AttendeeUser.objects.filter(username=identifier).first()
