from rest_framework.permissions import BasePermission
from django.http import HttpRequest
from rest_framework.exceptions import PermissionDenied


# Internal app-specific scope rules
ROLE_SCOPES = {
    'attendee': ['forgot:view'],
    'staff': ['forgot:view', 'forgot:create'],
    'admin': ['*'],  # wildcard: full access
}


class HasScopePermission(BasePermission):
    """
    Checks if the user's role (from JWT) includes the required scope for this endpoint.
    """
    required_scopes = None

    def has_permission(self, request: HttpRequest, view):
        token = request.auth
        role = token.get('role')

        allowed_scopes = ROLE_SCOPES.get(role, [])
        required_scopes = getattr(
            view, 'required_scopes', self.required_scopes)

        missing_scopes = [
            scope for scope in required_scopes if scope not in allowed_scopes]

        if missing_scopes:
            raise PermissionDenied()

        return any(scope in allowed_scopes for scope in required_scopes)
