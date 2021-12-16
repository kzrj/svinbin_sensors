# -*- coding: utf-8 -*-
import datetime
import requests
import json
import demjson
from calendar import monthrange

from mainapp.models import Sensor, SensorValue

# Servises SensorValues
def create_sensors_raw_values_dict(input_raw_list):
    sensor_value_ids = list()
    sensors_raw_values_dict = dict()

    for sensor in Sensor.objects.all().order_by('pk'):
        if sensor.value_id in sensors_raw_values_dict.keys():
            sensors_raw_values_dict[sensor.value_id]['sensors'].append(sensor)

        else:
            sensors_raw_values_dict[sensor.value_id] = {'raw_values': list(), 'sensors': [sensor]}
            sensor_value_ids.append(sensor.value_id)

    for raw_value in input_raw_list:
        if raw_value['id'] in sensor_value_ids:
            sensors_raw_values_dict[raw_value['id']]['raw_values'].append(raw_value)

    return sensors_raw_values_dict


def prepare_part_for_bulk_create_list(sensor, raw_data_list):
    sensor_raw_model_list = list()
    for raw_data in raw_data_list:
        sensor_raw_model_list.append(
            SensorValue(sensor=sensor, value=raw_data[sensor.value_key], 
                date=datetime.datetime.fromtimestamp(raw_data['ts'] / 1000))
            )
    return sensor_raw_model_list


def bulk_create_from_raw_values_dict(sensors_raw_values_dict):
    data_for_bulk_create = []

    for raw_dict_list_key in sensors_raw_values_dict.keys():
        raw_values = sensors_raw_values_dict[raw_dict_list_key]['raw_values']
        if len(raw_values) > 0:
            sensors = sensors_raw_values_dict[raw_dict_list_key]['sensors']

            if len(sensors) > 1:
                for sensor in sensors:
                    data_for_bulk_create = data_for_bulk_create + \
                        prepare_part_for_bulk_create_list(
                            sensor=sensor, raw_data_list=raw_values)
            else:
                data_for_bulk_create = data_for_bulk_create + \
                    prepare_part_for_bulk_create_list(
                        sensor=sensors[0], raw_data_list=raw_values)

    SensorValue.objects.bulk_create(data_for_bulk_create, ignore_conflicts=True)


def get_sensors_data(dt1, dt2):
    dt1_ts = int(datetime.datetime.timestamp(dt1) * 1000)
    dt2_ts = int(datetime.datetime.timestamp(dt2) * 1000)

    url = f'http://hahenty.ru:88/logs/{dt1_ts}/{dt2_ts}'
    r = requests.get(url)
    print(r.status_code)
    json_data = demjson.decode(r.text)
    print(len(json_data))

    return json_data


def create_values_by_month(month_number):
    mrange = monthrange(2021, month_number)

    for i in range(1, mrange[1] + 1):
        dt1 = datetime.datetime(2021, month_number, i, 0, 0, 0)
        print('start ', dt1)
        dt2 = dt1 + datetime.timedelta(days=1)
        input_data = get_sensors_data(dt1=dt1, dt2=dt2)

        sensors_raw_values_dict = create_sensors_raw_values_dict(
            input_raw_list=input_data)
        bulk_create_from_raw_values_dict(
                sensors_raw_values_dict=sensors_raw_values_dict)
