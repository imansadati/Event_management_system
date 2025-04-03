from django.db import models


class EmailLog(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=256)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.recipient} - {self.status}'
