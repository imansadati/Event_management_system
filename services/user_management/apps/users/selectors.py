from .models import AdminUser, StaffUser
from .filters import AdminFilter, StaffFilter


def user_admin_list(*, filters):
    filters = filters or {}

    qs = AdminUser.objects.all()
    return AdminFilter(filters, qs).qs


def user_staff_list(*, filters):
    filters = filters or {}

    qs = StaffUser.objects.all()
    return StaffFilter(filters, qs).qs
