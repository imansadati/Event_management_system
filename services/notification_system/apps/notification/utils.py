from .services import create_email_log, save_failed_emails_to_redis


def send_email(recipient, subject, body):
    try:
        # Simulate email sending (Replace with actual SMTP call)
        print(f"Sending email to {recipient}: {subject}")

        create_email_log(recipient=recipient, subject=subject,
                         body=body, status='sent')
        return True

    except Exception as e:
        create_email_log(recipient, subject, body,
                         status='failed', error=str(e))
        save_failed_emails_to_redis(
            {'recipient': recipient, 'subject': subject, 'body': body})
        return False
