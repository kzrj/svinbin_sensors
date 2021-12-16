# -*- coding: utf-8 -*-
import datetime
from celery import shared_task

from mainapp.servises import get_sensors_data, create_sensors_raw_values_dict, \
	bulk_create_from_raw_values_dict


@shared_task
def task_get_day_eng_data():
	dt1 = datetime.datetime.now()
    dt2 = dt1 - datetime.timedelta(days=1)

	input_data = get_sensors_data(dt1=dt1, dt2=dt2)
    sensors_raw_values_dict = create_sensors_raw_values_dict(
    input_raw_list=input_data)
    bulk_create_from_raw_values_dict(
            sensors_raw_values_dict=sensors_raw_values_dict)
