from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")

app.conf.task_acks_late = True
app.conf.task_default_priority = 5

app.conf.task_routes = {
    'apps.notification.tasks': {
        'queue': 'email_queue', 'routing_key': 'email_queue'
    }
}

app.autodiscover_tasks()
