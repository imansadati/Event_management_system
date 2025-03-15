from .models import AdminUser, StaffUser, AttendeeUser
from django.db import transaction
from shared_utils.update_model import model_update
from rest_framework.exceptions import ValidationError


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


@transaction.atomic
def user_admin_update(*, user: AdminUser, data):
    non_side_effect_fields = [
        "email",
        "full_name",
    ]

    try:
        updated_user = model_update(
            instance=user, fields=non_side_effect_fields, data=data
        )
        return updated_user
    except ValidationError as e:
        raise e


@transaction.atomic
def user_staff_update(*, user: StaffUser, data):
    non_side_effect_fields = [
        "email",
        "full_name",
        "availability_status",
    ]

    try:
        updated_user = model_update(
            instance=user, fields=non_side_effect_fields, data=data
        )
        return updated_user
    except ValidationError as e:
        raise e


@transaction.atomic
def user_attendee_update(*, user: AttendeeUser, data):
    non_side_effect_fields = [
        "email",
        "full_name",
    ]

    try:
        updated_user = model_update(
            instance=user, fields=non_side_effect_fields, data=data
        )
        return updated_user
    except ValidationError as e:
        raise e
