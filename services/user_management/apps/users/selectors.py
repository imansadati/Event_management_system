from .models import AdminUser
from .filters import AdminFilter


def user_admin_list(*, filters):
    filters = filters or {}

    qs = AdminUser.objects.all()
    return AdminFilter(filters, qs).qs
