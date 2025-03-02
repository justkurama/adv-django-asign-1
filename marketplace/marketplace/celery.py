import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

celery_app = Celery('marketplace')

# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
