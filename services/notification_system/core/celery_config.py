from celery import Celery  # type: ignore
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")

app.conf.task_acks_late = True
app.conf.task_routes = {

}

app.autodiscover_tasks()
