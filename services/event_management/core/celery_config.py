from celery import Celery
import os
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")

app.conf.task_acks_late = True
app.conf.task_default_priority = 5

app.conf.task_routes = (
    Queue(
        'event_publish_queue',
        routing_key='event_publish_queue',
        queue_arguments={'x-max-priority': 10}
    )
)

app.autodiscover_tasks(['apps.events'])
