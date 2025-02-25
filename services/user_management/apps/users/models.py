from django.contrib.auth.models import BaseUserManager as BUM


class BaseUserManager(BUM):
    def create_user(self, full_name: str, email: str, password: str, **extra_fields):
        if not email:
            return ValueError('Users must have an email address')

        email = self.normalize_email(email.lower())

        user = self.model(
            full_name=full_name,
            email=email,
            **extra_fields
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password(password)

        user.full_clean()
        user.save(using=self._db)
        return user
