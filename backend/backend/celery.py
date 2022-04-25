from __future__ import absolute_import
from datetime import timedelta
import os
from re import A
from celery import Celery

from celery.schedules import crontab # scheduler

# default django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.conf.timezone = 'UTC'

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    'every-15-seconds': {
        'task': 'api.tasks.get_google_news',
        'schedule': 10,
    }
}

app.autodiscover_tasks()




# app.conf.beat_schedule = {
#     # executes every 1 minute
#     'scraping-task-one-min': {
#         'task': 'tasks.get_google_news',
#         'schedule': crontab(),
#     }
# }
    # # executes every 15 minutes
    # 'scraping-task-fifteen-min': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute='*/15')
    # },
    # # executes daily at midnight
    # 'scraping-task-midnight-daily': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute=0, hour=0)
    # }
