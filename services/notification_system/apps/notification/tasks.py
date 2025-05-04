from celery import shared_task
from .services import create_email_log, save_failed_emails_to_redis
from .redis_client import redis_client
import json


@shared_task(bind=True, max_retries=3, default_retry_delay=45)
def send_email_task(self, recipient, subject, body):
    try:
        # Simulate email sending (Replace with actual SMTP call)

        create_email_log(recipient=recipient, subject=subject,
                         body=body, status='sent')
        print(f"Email sent: {recipient} - {subject}")
    except Exception as e:
        if self.request.retries >= self.max_retries:
            print(f"[Error] Failed to send email: {str(e)}")
            create_email_log(recipient, subject, body,
                             status='failed', error=str(e))
            save_failed_emails_to_redis(
                {'recipient': recipient, 'subject': subject, 'body': body})
        raise self.retry(exc=e)


# retry failed emails in redis using celery beats
@shared_task
def retry_failed_emails():
    failed_emails = redis_client.select(
        2) and redis_client.lrange('email_queue', 0, -1)

    if not failed_emails:
        print("No failed emails to retry.")
        return

    for raw_email in failed_emails:
        email_data = json.loads(raw_email)
        success = send_email_task.delay(**email_data)
        if success:
            redis_client.lrem('email_queue', 0, raw_email)
