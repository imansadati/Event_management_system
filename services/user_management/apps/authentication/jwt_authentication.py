from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.models import AttendeeUser, StaffUser, AdminUser
from django.db.models import Q
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """Override get_user() to support multiple user models."""
        user_id = validated_token.get('user_id')

        if not user_id:
            return None

        user = (
            AttendeeUser.objects.filter(Q(id=user_id) & Q(is_attendee=True)).first() or
            AdminUser.objects.filter(Q(id=user_id) & Q(is_admin=True)).first() or
            StaffUser.objects.filter(Q(id=user_id) & Q(is_staff=True)).first()
        )

        if user:
            return user
        raise AuthenticationFailed(detail='User not found.')
