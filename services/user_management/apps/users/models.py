from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
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


class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, unique=True, db_index=True)
    full_name = models.CharField(max_length=128, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='%(class)s_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='%(class)s_permissions',
        blank=True,
    )

    USERNAME_FIELD = 'username'

    objects = BaseUserManager()

    class Meta:
        abstract = True
