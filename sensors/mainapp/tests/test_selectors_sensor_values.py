# -*- coding: utf-8 -*-
import datetime

from django.db.models import Q, Prefetch
from django.test import TransactionTestCase

from mainapp.models import Location, Sensor, SensorValue, Workshop
from mainapp import servises, selectors
from core.utils import init_locations, init_sensors


class SensorValueSelectorsTest(TransactionTestCase):
    def setUp(self):
        init_locations()
        init_sensors()

        input_list = [
            {
                "ts": 1630425600000,
                "id": "shop1/pair1/temperature/regular",
                "temperature": 19.4
              },
            {
                "ts": 1630425600000,
                "id": "shop1/pair2/temperature/regular",
                "temperature": 24.2
              },
            {
                "ts": 1630425600000,
                "id": "shop3/section2/temperature/regular",
                "temperature": 25.3
              },
            {
                "ts": 1630425600000,
                "id": "shop3/section5/temperature/regular",
                "temperature": 26.5
              },
            {
                "ts": 1630425600000,
                "id": "shop4/section4/temperature/regular",
                "temperature": 22.3
              },
            {
                "ts": 1630425600000,
                "id": "shop4/section6/temperature/regular",
                "temperature": 21.4
              },
            {
                "ts": 1630425600000,
                "id": "shop7/section4/temperature/regular",
                "temperature": 21.9
              },
        ]
        sensors_raw_values_dict = servises.create_sensors_raw_values_dict(
            input_raw_list=input_list)

        servises.bulk_create_from_raw_values_dict(
            sensors_raw_values_dict=sensors_raw_values_dict)

    def test_get_temp_deviations_by_workshop(self):
        t_min = 20
        t_max = 24
        d1 = datetime.date(2021, 8, 31)
        d2 = datetime.date(2021, 9, 1)
     
        workshops = selectors.get_temp_deviations_by_workshops(t_min=t_min, t_max=t_max, d1=d1, d2=d2)

        with self.assertNumQueries(4):
            for ws in workshops:
                bool(ws.filtered_locs)
                for loc in ws.filtered_locs:
                    bool(loc.filtered_sensors)
                    for sensor in loc.filtered_sensors:
                        bool(sensor.filtered_values)