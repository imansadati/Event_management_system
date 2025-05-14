

# Internal app-specific scope rules
ROLE_SCOPES = {
    'attendee': ['forgot:view'],
    'staff': ['forgot:view', 'forgot:create'],
    'admin': ['*'],  # wildcard: full access
}
