from django.db import models


class EventManager(models.Manager):
    def create_event(self, **kwargs):
        kwargs.setdefault('status', 'draft')
        kwargs.setdefault('type', 'public')
        kwargs.setdefault('gallery', [])

        event = self.model(**kwargs)

        event.full_clean()
        event.save(using=self._db)
        return event


class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),  # jsut show published events
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
    category = models.ForeignKey(
        'EventCategory', on_delete=models.SET_NULL, null=True, related_name='events')
    cover_images = models.ImageField(
        upload_to='images/events/', null=True, blank=True)
    gallery = models.JSONField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)  # for online events
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = EventManager()

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self):
        return self.title


# all type of events (concerts, sport events, workshops, ...)
class EventCategory(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
