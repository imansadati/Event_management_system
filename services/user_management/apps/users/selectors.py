from .models import AdminUser, StaffUser, AttendeeUser
from .filters import AdminFilter, StaffFilter, AttendeeFilter
from django.shortcuts import get_object_or_404


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


def user_admin_get(user_id):
    return get_object_or_404(AdminUser, id=user_id)


def user_staff_get(user_id):
    return get_object_or_404(StaffUser, id=user_id)


def user_attendee_get(user_id):
    return get_object_or_404(AttendeeUser, id=user_id)
