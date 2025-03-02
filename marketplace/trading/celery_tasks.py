from celery.schedules import crontab
from celery import Celery
from .tasks import process_pending_orders, generate_sales_report

app = Celery('trading')

app.conf.beat_schedule = {
    'process_orders_every_10s': {
        'task': 'trading.tasks.process_pending_orders',
        'schedule': 10.0,  # Run every 10 seconds
    },
    'generate_reports_daily': {
        'task': 'trading.tasks.generate_sales_report',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}
