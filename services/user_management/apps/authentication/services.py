from .selectors import get_user_by_identifier
from rest_framework_simplejwt.tokens import RefreshToken


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
