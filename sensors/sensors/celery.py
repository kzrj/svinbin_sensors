# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensors.settings')
app = Celery('sensors', broker='amqp://admin:qwerty123@rabbit:5672', backend='rpc://')
    
# app.conf.broker_heartbeat = 0

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()