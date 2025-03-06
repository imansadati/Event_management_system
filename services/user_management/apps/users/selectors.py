from .models import AdminUser, StaffUser, AttendeeUser
from .filters import AdminFilter, StaffFilter, AttendeeFilter
from django.http import Http404
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
    try:
        return get_object_or_404(AdminUser, id=user_id)
    except Http404:
        return None


def user_staff_get(user_id):
    try:
        return get_object_or_404(StaffUser, id=user_id)
    except Http404:
        return None


def user_attendee_get(user_id):
    try:
        return get_object_or_404(AttendeeUser, id=user_id)
    except Http404:
        return None
