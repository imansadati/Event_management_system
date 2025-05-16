from .selectors import get_user_by_identifier
from .redis_client import redis_client
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.db import transaction
import jwt
from datetime import datetime


def authenticate_user(identifier: str, password: str):
    """Authenticate the user by checking credentials."""
    user = get_user_by_identifier(identifier)

    if not user or not user.check_password(password):
        return None
    return user


def is_refreshtoken_blacklisted(refresh_token):
    """Check if the given token is blacklisted in Redis."""
    return redis_client.exists(f'blacklist:{refresh_token}')


def blacklist_refreshtoken(refresh_token):
    """store refresh token in blacklist redis."""
    redis_client.setex(
        f'blacklist:{refresh_token}', int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()), '1')


@transaction.atomic
def update_password(user, new_password):
    try:
        user.set_password(new_password)
        user.save()
    except ValidationError as e:
        raise ValidationError(e)


def generate_specific_token(email, type, id=None, role=None):
    """
    For specific actions, generate a specific token for the submitted user.
    This is not used for authentication.
    """
    payload = {
        'user_id': id,
        'email': email,
        'exp': datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        'type': type,
        'role': role
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def verify_specific_token(token, type):
    """
    Verify that specific token by checking the type, expiration and validation.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if payload['type'] != type:
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
