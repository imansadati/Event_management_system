from .models import AdminUser
from django.db import transaction


@transaction.atomic
def user_admin_create(*, email, username, password, full_name):
    user = AdminUser.objects.create_admin(
        email=email, full_name=full_name, username=username, password=password)
    return user
