from .selectors import get_user_by_identifier, get_user_by_id
from rest_framework_simplejwt.tokens import RefreshToken
from .redis_client import redis_client
from django.conf import settings


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


def refreshtoken_blacklist_processing(refresh_token):
    """Validate and store refresh token in blacklist redis."""
    token = RefreshToken(refresh_token)

    user_id = token['user_id']
    user = get_user_by_id(user_id)
    if user:
        new_refresh_token = generate_tokens(user)
        redis_client.setex(
            f'blacklist:{refresh_token}', int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()), '1')

        return new_refresh_token
    return None
