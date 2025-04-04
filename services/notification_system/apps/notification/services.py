from .models import EmailLog
from django.db import transaction
from .redis_client import redis_client
import json


@transaction.atomic
def create_email_log(recipient, subject, message, status, error=None):
    EmailLog.objects.create(recipient=recipient, subject=subject,
                            message=message, status=status, error=error)


def save_failed_emails_to_redis(email_data):
    redis_client.rpush('email_queue', json.dumps(email_data))
