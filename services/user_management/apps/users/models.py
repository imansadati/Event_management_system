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


class AdminUser(BaseUser):
    profile = models.OneToOneField(
        'Profile', on_delete=models.CASCADE, blank=True, null=True)
    is_admin = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'admin'
        verbose_name_plural = 'admins'

    def __str__(self):
        return self.full_name


class AttendeeUser(BaseUser):
    profile = models.OneToOneField(
        'Profile', on_delete=models.CASCADE, null=True, blank=True)
    membership_status = models.CharField(
        max_length=16, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    is_attendee = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'attendee'
        verbose_name_plural = 'attendees'

    def __str__(self):
        return self.full_name


class StaffUser(BaseUser):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=True)
    job_title = models.CharField(max_length=64)
    availability_status = models.CharField(
        max_length=32, choices=[('available', 'Available'), ('busy', 'Busy')])
    work_experience = models.SmallIntegerField()

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff'

    def __str__(self):
        return self.full_name


class Profile(models.Model):
    picture = models.ImageField(
        upload_to='images/profile/', blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=8, choices=[
                              ('male', 'Male'), ('female', 'Female')])
