from django.db import models
from django.db.models import JSONField
from apps.session.models import Session


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
        max_length=16, choices=SPEAKER_TYPES, default='other')
    photo = models.ImageField(
        upload_to='images/speaker/', blank=True, null=True)
    socials = JSONField(blank=True, null=True)
    status = models.CharField(
        max_length=16, choices=STATUS_TYPES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SessionSpeaker(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('session', 'speaker')
