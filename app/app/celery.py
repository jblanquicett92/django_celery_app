from __future__ import absolute_import, unicode_literals

from celery import Celery


import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = 'America/Mexico_City'

app.autodiscover_tasks()
