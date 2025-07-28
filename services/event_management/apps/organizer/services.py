from .models import Organizer, OrganizerMember
from django.db import transaction
from shared_utils.update_model import model_update
from rest_framework.exceptions import ValidationError


@transaction.atomic()
def organizer_create(**kwargs):
    organizer = Organizer.objects.create(**kwargs)

    return organizer


def organizer_update(*, organizer: Organizer, data):
    non_side_effect_fields = [
        'name',
        'website'
    ]

    try:
        updated_organizer = model_update(
            instance=organizer, fields=non_side_effect_fields, data=data
        )
        return updated_organizer
    except ValidationError as e:
        raise e


@transaction.atomic()
def organizer_member_create(**kwargs):
    member = OrganizerMember.objects.create(**kwargs)

    return member


def organizer_member_update(*, member: OrganizerMember, data):
    non_side_effect_fields = [
        'role'
    ]

    try:
        updated_organizer_member = model_update(
            instance=member, fields=non_side_effect_fields, data=data
        )
        return updated_organizer_member
    except ValidationError as e:
        raise e
