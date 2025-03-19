from apps.users.models import AttendeeUser


def get_user_by_identifier(identifier):
    if '@' in identifier:
        return AttendeeUser.objects.filter(email=identifier).first()
    return AttendeeUser.objects.filter(username=identifier).first()
