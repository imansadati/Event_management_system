from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")

app.conf.task_acks_late = True
app.conf.task_default_priority = 5

app.conf.task_routes = {
    'apps.events.tasks': {
        'queue': 'publish_event_queue', 'routing_key': 'publish_event_queue'
    }
}

app.conf.task_default_queue = 'publish_event_queue'
app.autodiscover_tasks(['apps.events'])
