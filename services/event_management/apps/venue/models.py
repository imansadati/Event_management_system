from django.db import models


class Venue(models.Model):
    VENUE_TYPES = [
        ('auditorium', 'Auditorium'),
        ('conference_room', 'Conference Room'),
        ('stadium', 'Stadium'),
        ('outdoor', 'Outdoor'),
        ('other', 'Other'),
    ]
    STATUS_TYPES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived')
    ]
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    venue_type = models.CharField(
        max_length=20, choices=VENUE_TYPES, default='other')
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_TYPES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.city}'
