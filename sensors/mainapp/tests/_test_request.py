# -*- coding: utf-8 -*-
import datetime
import requests
import json
import demjson
from calendar import monthrange


def get_sensors_data(dt1):
    dt1_ts = int(datetime.datetime.timestamp(dt1) * 1000)
    dt2 = dt1 + datetime.timedelta(days=1)
    dt2_ts = int(datetime.datetime.timestamp(dt2) * 1000)

    url = f'http://hahenty.ru:88/logs/{dt1_ts}/{dt2_ts}'
    r = requests.get(url)
    print(r.status_code)
    # print(r.text)
    # json_data = json.loads(r.text)
    json_data = demjson.decode(r.text)

    # json_data = []

    print(len(json_data))
    # print(dt1_ts, dt2_ts)

    return json_data


def get_by_month(month_number):
    final_list = list()
    mrange = monthrange(2021, month_number)

    for i in range(mrange[0], mrange[1] + 1):
        dt1 = datetime.datetime(2021, month_number, i, 0, 0, 0)
        print('start ', dt1)
        final_list = final_list + get_sensors_data(dt1=dt1)

    return final_list

final_list = get_by_month(month_number=6)

# dt1 = datetime.datetime(2021, 6, 22, 0, 0, 0)
# final_list = get_sensors_data(dt1=dt1)

print(len(final_list))



