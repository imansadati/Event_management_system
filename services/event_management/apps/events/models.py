from django.db import models


class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    TYPE_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ('invite_only', 'Invite only'),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField()
    capacity = models.IntegerField(null=True, blank=True)
    type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, default='public')
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default='draft')
    cover_images = models.ImageField(
        upload_to='images/events/', null=True, blank=True)
    gallery = models.JSONField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)  # for online events
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self):
        return self.title
