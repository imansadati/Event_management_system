from celery import shared_task
from .services import create_email_log, save_failed_emails_to_redis


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
