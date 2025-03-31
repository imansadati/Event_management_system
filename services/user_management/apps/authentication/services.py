from .selectors import get_user_by_identifier
from rest_framework_simplejwt.tokens import RefreshToken
from .redis_client import redis_client
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.db import transaction


def authenticate_user(identifier: str, password: str):
    """Authenticate the user by checking credentials."""
    user = get_user_by_identifier(identifier)

    if not user or not user.check_password(password):
        return None
    return user


def generate_tokens(user):
    """Generate JWT access and refresh tokens for a user"""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    return {
        'access_token': str(access_token),
        'refresh_token': str(refresh),
    }


def is_refreshtoken_blacklisted(refresh_token):
    """Check if the given token is blacklisted in Redis."""
    return redis_client.exists(f'blacklist:{refresh_token}')


def blacklist_refreshtoken(refresh_token):
    """Validate and store refresh token in blacklist redis and generate new tokens."""
    redis_client.setex(
        f'blacklist:{refresh_token}', int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()), '1')


@transaction.atomic
def update_password(user, new_password):
    try:
        user.set_password(new_password)
        user.save()
    except ValidationError as e:
        raise ValidationError(e)
