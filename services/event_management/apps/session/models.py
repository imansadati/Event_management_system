from django.db import models
from apps.events.models import Event
from apps.venue.models import Venue


class Session(models.Model):
    STATUS_TYPES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
    ACCESS_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('invite_only', 'Invite Only')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='sessions')
    venue = models.ForeignKey(
        Venue, on_delete=models.SET_NULL, null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    access_type = models.CharField(
        max_length=20, choices=ACCESS_TYPES, default='public')
    status = models.CharField(
        max_length=16, choices=STATUS_TYPES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
