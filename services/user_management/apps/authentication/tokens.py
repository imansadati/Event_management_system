from rest_framework_simplejwt.tokens import RefreshToken


ROLE_SCOPES = {
    'attendee': {},
    'admin': {},
    'staff': {}
}


def generate_jwt_tokens(user):
    """Generate JWT access and refresh tokens with scopes to check accesses for a user"""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    scopes = ROLE_SCOPES.get(user.role, [])

    refresh['role'] = user.role
    refresh['scopes'] = scopes
    refresh['email'] = user.email

    return {
        'access_token': str(access_token),
        'refresh_token': str(refresh),
    }
