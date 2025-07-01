from rest_framework.throttling import UserRateThrottle
from django.http import HttpRequest


class RoleBasedRateThrottle(UserRateThrottle):
    scope = 'role_based'

    def get_cache_key(self, request: HttpRequest, view):
        if not request.user or not request.user.is_authenticated:
            return super().get_cache_key(request, view)

        role = getattr(request.user, 'role', 'unknown')
        ident = f':{role}_{request.user.pk}'

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def allow_request(self, request: HttpRequest, view):
        # Dynamically decide rate based on role
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin':
                self.rate = '1000/day'  # change this for your needed.
            elif request.user.role == 'staff':
                self.rate = '1000/day'  # change this for your needed.
            elif request.user.role == 'attendee':
                self.rate = '1000/day'  # change this for your needed.
            else:
                self.rate = None
        else:
            self.rate = None

        if self.rate:
            self.num_requests, self.duration = self.parse_rate(self.rate)
        else:
            self.num_requests = self.duration = None

        return super().allow_request(request, view)
