
from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__, broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')


CELERY_BEAT_SCHEDULE = {
    'generate-monthly-report': {
        'task': 'tasks.generate_monthly_report',
        'schedule':30,
        # 'schedule': crontab(day_of_month=1), #for every first day of month
    },
    'daily-request-reminder': {
        'task': 'tasks.daily_request_reminder',
       'schedule': crontab(hour=20, minute=0),  #for every day at 8 PM
    },

}

celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE