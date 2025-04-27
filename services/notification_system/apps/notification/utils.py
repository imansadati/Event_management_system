from .services import create_email_log, save_failed_emails_to_redis


def send_email(recipient, subject, body):
    try:
        # Simulate email sending (Replace with actual SMTP call)

        create_email_log(recipient=recipient, subject=subject,
                         body=body, status='sent')
        print(f"Email sent: {recipient} - {subject}")
        return True

    except Exception as e:
        print(f"[Error] Failed to send email: {str(e)}")
        create_email_log(recipient, subject, body,
                         status='failed', error=str(e))
        save_failed_emails_to_redis(
            {'recipient': recipient, 'subject': subject, 'body': body})
        return False
