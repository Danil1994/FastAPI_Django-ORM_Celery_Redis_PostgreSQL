import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
API_KEY_BLOCKCHAIR = os.getenv("API_KEY_BLOCKCHAIR")
API_KEY_COINMARKETCAP = os.getenv("API_KEY_COINMARKETCAP")

celery_app = Celery("fastapi_app", broker=CELERY_BROKER_URL)
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.autodiscover_tasks(["fastapi_app.tasks"])

celery_app.conf.beat_schedule = {
    'fetch-eth-block-every-minute': {
        'task': 'fastapi_app.tasks.fetch_eth_block',
        'schedule': crontab(minute='*'),
        'args': (API_KEY_BLOCKCHAIR,),
    },
    'fetch-btc-block-every-minute': {
        'task': 'fastapi_app.tasks.fetch_btc_block',
        'schedule': crontab(minute='*'),
        'args': (API_KEY_COINMARKETCAP,),
    },
}
