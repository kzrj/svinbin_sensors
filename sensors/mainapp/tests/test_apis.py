# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from mainapp.models import Location, Sensor, SensorValue, Workshop
from mainapp import servises
from core.utils import init_locations, init_sensors


class SensorsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
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
        
    def test_temp_deviations_api(self):
        d1 = datetime.date(2021, 8, 31)
        d2 = datetime.date(2021, 9, 1)
        t_min = 20
        t_max = 24

        response = self.client.get(f'/api/deviations/?d1={d1}&d2={d2}&t_min={t_min}&t_max={t_max}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_deviations_filter(self):
        response = self.client.get(f'/api/values/?deviations_min=20&deviations_max=24')
        print(response.data)

