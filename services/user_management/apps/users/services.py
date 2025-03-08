from .models import AdminUser, StaffUser, AttendeeUser
from django.db import transaction


@transaction.atomic
def user_admin_create(*, email, username, password, full_name):
    user = AdminUser.objects.create_admin(
        email=email, full_name=full_name, username=username, password=password)
    return user


@transaction.atomic
def user_staff_create(*, email, username, password, full_name, job_title, work_experience):
    user = StaffUser.objects.create_staff(
        email=email, full_name=full_name, username=username, password=password, job_title=job_title, work_experience=work_experience)
    return user


@transaction.atomic
def user_attendee_create(*, email, username, password, full_name):
    user = AttendeeUser.objects.create_attendee(
        email=email, full_name=full_name, username=username, password=password)
    return user
