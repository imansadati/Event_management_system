from django.db import models
from apps.events.models import Event
from apps.venue.models import Venue
from apps.speaker.models import Speaker


class Session(models.Model):
    STATUS_TYPES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='sessions')
    venue = models.ForeignKey(
        Venue, on_delete=models.SET_NULL, null=True, blank=True)
    speakers = models.ManyToManyField(Speaker, related_name='sessions')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=16, choices=STATUS_TYPES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
