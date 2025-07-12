from celery import shared_task
from .selectors import event_get
from django.utils import timezone


@shared_task(bind=True, max_retries=3, default_retry_delay=45)
def publsih_event_task(self, event_id):
    try:
        event = event_get(event_id)
        if event.status != 'published' and event.published_at <= timezone.now():
            event.status = 'published'
            event.save(update_fields=['status'])

    except Exception as e:
        if self.request.retries >= self.max_retries:
            print(f"[Error] Failed to publish event: {str(e)}")
            # save failed events to redis (optional) see: notification_system/apps/notifications/tasks.py
        raise self.retry(exc=e)
