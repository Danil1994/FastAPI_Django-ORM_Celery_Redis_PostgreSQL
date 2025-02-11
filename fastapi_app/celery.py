import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastapi_app.settings')
django.setup()

from celery import Celery

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("../fastapi_app", broker=CELERY_BROKER_URL)

celery_app.autodiscover_tasks(["fastapi_app.tasks"])
