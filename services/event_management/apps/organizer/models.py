from django.db import models

# Create your models here.


class Organizer(models.Model):
    TYPE_CHOICES = [
        ('company', 'Company'),
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]

    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, default='individual')
    logo = models.ImageField(upload_to='images/organizer/', blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name


class OrganizerMember(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('manager', 'Manager')
    ]

    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    role = models.CharField(
        max_length=16, choices=ROLE_CHOICES, default='manager')
    added_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.organizer.name
