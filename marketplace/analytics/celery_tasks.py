from celery.schedules import crontab
from celery import Celery
from analytics.tasks import generate_daily_reports

app = Celery('analytics')

app.conf.beat_schedule = {
    'generate_reports_daily': {
        'task': 'analytics.tasks.generate_daily_reports',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}
