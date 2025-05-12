from rest_framework_simplejwt.tokens import RefreshToken


ROLE_SCOPES = {
    'attendee': {},
    'admin': {},
    'staff': {}
}


def generate_jwt_tokens(user):
    """Generate JWT access and refresh tokens with scopes to check accesses for a user"""
    pass
