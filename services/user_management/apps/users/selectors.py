from .models import AdminUser, StaffUser, AttendeeUser
from .filters import AdminFilter, StaffFilter, AttendeeFilter


def user_admin_list(*, filters):
    filters = filters or {}

    qs = AdminUser.objects.all()
    return AdminFilter(filters, qs).qs


def user_staff_list(*, filters):
    filters = filters or {}

    qs = StaffUser.objects.all()
    return StaffFilter(filters, qs).qs


def user_attendee_list(*, filters):
    filters = filters or {}

    qs = AttendeeUser.objects.all()
    return AttendeeFilter(filters, qs).qs
