from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_tokens(user):
    """Generate JWT access and refresh tokens with assigning role claim for a user"""
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    access_token['role'] = user.role
    access_token['email'] = user.email

    return {
        'access_token': str(access_token),
        'refresh_token': str(refresh),
    }
