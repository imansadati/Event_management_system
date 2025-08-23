from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """Override get_user() to support multiple user sources (models or gRPC)."""
        role = validated_token.get('role')
        user_id = validated_token.get('user_id')

        if not role or not user_id:
            raise AuthenticationFailed('Token missing role or user_id')

        role_model_map = getattr(settings, 'JWT_ROLE_MODEL_MAP', None)
        if not isinstance(role_model_map, dict):
            raise ImproperlyConfigured(
                'JWT_ROLE_MODEL_MAP must be a dictionary in settings.py')

        model_info = role_model_map.get(role)
        if not model_info:
            raise AuthenticationFailed(
                f'Role {role} not found in JWT_ROLE_MODEL_MAP')

        try:
            # Case 1: Django model (tuple format: ('app_label', 'ModelName'))
            if isinstance(model_info, tuple) and len(model_info) == 2:
                app_label, model_path = model_info
                model = apps.get_model(app_label, model_path)
                if not model:
                    raise AuthenticationFailed(
                        f'Model {model_path} not found for role {role}')

                status_flag = f'is_{role}'
                user = model.objects.filter(
                    id=user_id, **{status_flag: True}).first()

                if user:
                    return user
                raise AuthenticationFailed('User not found or inactive.')

            # Case 2: Remote gRPC client
            elif hasattr(model_info, 'get_user'):
                user_data = model_info.get_user(user_id, role)
                if user_data:
                    return user_data
                raise AuthenticationFailed('Remote user not found.')

            else:
                raise ImproperlyConfigured(
                    f'Invalid JWT_ROLE_MODEL_MAP entry for role {role}: {model_info}'
                )

        except Exception as e:
            raise AuthenticationFailed(f'Authentication error: {str(e)}')
