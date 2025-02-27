from .models import AdminUser


def user_admin_list():

    qs = AdminUser.objects.all()
    return qs
