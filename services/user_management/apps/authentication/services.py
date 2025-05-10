from .selectors import get_user_by_identifier
from rest_framework_simplejwt.tokens import RefreshToken
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


def generate_reset_password_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        'type': 'password_reset'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def verify_reset_password_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
        if payload['type'] != 'password_reset':
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
