from django.db import models
from django.db.models import JSONField


class Speaker(models.Model):
    SPEAKER_TYPES = [
        ('keynote', 'Keynote Speaker'),
        ('guest', 'Guest Speaker'),
        ('panelist', 'Panelist'),
        ('host', 'Host'),
        ('moderator', 'Moderator'),
        ('other', 'Other'),
    ]
    STATUS_TYPES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('draft', 'Draft'),
    ]

    name = models.CharField(max_length=128)
    bio = models.TextField(blank=True)
    type = models.CharField(
        max_length=16, choices=SPEAKER_TYPES, default='others')
    photo = models.ImageField(
        upload_to='images/speaker/', blank=True, null=True)
    socials = JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=16, choices=STATUS_TYPES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# * TODO: After create session app and complete model must Add SessionSpeaker model
