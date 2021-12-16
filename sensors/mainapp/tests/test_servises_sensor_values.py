# -*- coding: utf-8 -*-
import datetime

from django.test import TransactionTestCase

from mainapp.models import Location, Sensor, SensorValue
from mainapp import servises
from core.utils import init_locations, init_sensors


class SensorValueServisesTest(TransactionTestCase):
    def setUp(self):
        init_locations()
        init_sensors()

        self.input_list = [
            {
                "ts": 1630425600000,
                "id": "pumps/common/watercounter/regular",
                "input1": 18664,
                "input2": 18587,
                "input3": 0,
                "input4": 0,
                "consumption": 37251
            },
            {
                "ts": 1630425621122,
                "id": "pumps/water/pressure",
                "pressure": 4.047,
                "cwspressure": 0
            },
            {
                "ts": 1630426229162,
                "id": "pumps/house",
                "automode": True,
                "househeat": False,
                "voltageon": False,
                "insidetemperature": 25.9,
                "outsidetemperature": 15.4,
                "electrocountreadings": 0
            },
            {
                "ts": 1630447200000,
                "id": "pumps/house",
                "automode": True,
                "househeat": False,
                "voltageon": False,
                "insidetemperature": 28.9,
                "outsidetemperature": 17.4,
                "electrocountreadings": 0
            },
            {
                "ts": 1630447200000,
                "id": "pumps/house",
                "automode": True,
                "househeat": False,
                "voltageon": False,
                "insidetemperature": 29.3,
                "outsidetemperature": 18.9,
                "electrocountreadings": 0
            },
            {
                "ts": 1630447200000,
                "id": "pumps/well/watercounter/regular",
                "input1": 338941,
                "input2": 0,
                "input3": 0,
                "input4": 0,
                "consumption": 338.941
            },
            {
                "ts": 1630468800000,
                "id": "pumps/ecofood/watercounter/regular",
                "input1": 349772,
                "input2": 0,
                "input3": 0,
                "input4": 0,
                "consumption": 3497.72
            },
        ]

    def test_create_sensors_raw_values_dict(self):
        '''
            sensors_raw_values_dict should be like = {
                "pumps/common/watercounter/regular": {"raw_values": [ ... ], "sensors": [ ... ]},
                "pumps/ecofood/watercounter/regular": {"raw_values": [ ... ], "sensors": [ ... ]},
                ...
            }
        '''
        with self.assertNumQueries(1):
            sensors_raw_values_dict = servises.create_sensors_raw_values_dict(
                input_raw_list=self.input_list)

        self.assertEqual(len(list(sensors_raw_values_dict.keys())), 
            len(list(set(Sensor.objects.all().values_list('value_id', flat=True)))))

        self.assertEqual(
            len(sensors_raw_values_dict['pumps/common/watercounter/regular']['raw_values']), 1)
        self.assertEqual(
            len(sensors_raw_values_dict['pumps/common/watercounter/regular']['sensors']), 1)

        self.assertEqual(len(sensors_raw_values_dict['pumps/house']['raw_values']), 3)
        self.assertEqual(len(sensors_raw_values_dict['pumps/house']['sensors']), 2)

        self.assertEqual(
            len(sensors_raw_values_dict['shop1/pair1/temperature/regular']['raw_values']), 0)
        self.assertEqual(
            len(sensors_raw_values_dict['shop1/pair1/temperature/regular']['sensors']), 1)

    def test_prepare_part_for_bulk_create_list(self):
        input_data = [
            {
                "ts": 1630426229162,
                "id": "pumps/house",
                "automode": True,
                "househeat": False,
                "voltageon": False,
                "insidetemperature": 25.9,
                "outsidetemperature": 15.4,
                "electrocountreadings": 0
            },
            {
                "ts": 1630447200000,
                "id": "pumps/house",
                "automode": True,
                "househeat": False,
                "voltageon": False,
                "insidetemperature": 28.9,
                "outsidetemperature": 17.4,
                "electrocountreadings": 0
            },
            {
                "ts": 1630447200000,
                "id": "pumps/house",
                "automode": True,
                "househeat": False,
                "voltageon": False,
                "insidetemperature": 30.9,
                "outsidetemperature": 17.4,
                "electrocountreadings": 0
            },
        ]

        sensor1 = Sensor.objects.get(value_id='pumps/house', value_key='insidetemperature')
        sensor1_raw_model_list = servises.prepare_part_for_bulk_create_list(
            sensor=sensor1, raw_data_list=input_data)

        self.assertEqual(len(sensor1_raw_model_list), 3)
        self.assertEqual(sensor1_raw_model_list[0].sensor, sensor1)
        self.assertEqual(sensor1_raw_model_list[0].value, 25.9)

        sensor2 = Sensor.objects.get(value_id='pumps/house', value_key='outsidetemperature')
        sensor2_raw_model_list = servises.prepare_part_for_bulk_create_list(
            sensor=sensor2, raw_data_list=input_data)

        self.assertEqual(len(sensor2_raw_model_list), 3)
        self.assertEqual(sensor2_raw_model_list[0].sensor, sensor2)
        self.assertEqual(sensor2_raw_model_list[0].value, 15.4)

    def test_bulk_create_from_raw_values_dict(self):
        sensors_raw_values_dict = servises.create_sensors_raw_values_dict(
            input_raw_list=self.input_list)

        with self.assertNumQueries(1):
            servises.bulk_create_from_raw_values_dict(
                sensors_raw_values_dict=sensors_raw_values_dict)

        # input data for 10 values, but two records has same datetime so 8 values
        self.assertEqual(SensorValue.objects.all().count(), 8)

        sensor1 = Sensor.objects.get(value_id='pumps/house', value_key='insidetemperature')
        values = list(SensorValue.objects.filter(sensor=sensor1).order_by('pk'))
        self.assertEqual(len(values), 2)
        self.assertEqual(values[0].value, 25.9)
        self.assertEqual(values[1].value, 28.9)

    def test_ws1_2_sensor_values(self):
        input_data = [{
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
            "id": "shop2/pair1/temperature/regular",
            "temperature": 25.5
            },]

        sensors_raw_values_dict = servises.create_sensors_raw_values_dict(
            input_raw_list=input_data)
        servises.bulk_create_from_raw_values_dict(
                sensors_raw_values_dict=sensors_raw_values_dict)
        sensor1 = Sensor.objects.get(value_id='shop1/pair1/temperature/regular',
             value_key='temperature')
        sensor1_value = SensorValue.objects.filter(sensor=sensor1).first()
        self.assertEqual(SensorValue.objects.filter(sensor=sensor1).count(), 1)
        self.assertEqual(sensor1_value.value, 19.4)

        self.assertEqual(SensorValue.objects.all().count(), 3)

    def test_ws5_sensor_values(self):
        input_data = [{
                "ts": 1630425600000,
                "id": "shop5/section1&4/temperature/regular",
                "temperature": 20.2
            },
            {
                "ts": 1630425600000,
                "id": "shop5/section2&3/temperature/regular",
                "temperature": 25.2
            },
            {
                "ts": 1630425600000,
                "id": "shop5/section1/counter/regular",
                "consumption": 2468.1668,
                "temperature": 22
            },
        ]

        sensors_raw_values_dict = servises.create_sensors_raw_values_dict(
            input_raw_list=input_data)
        servises.bulk_create_from_raw_values_dict(
                sensors_raw_values_dict=sensors_raw_values_dict)

        self.assertEqual(SensorValue.objects.all().count(), 5)
        self.assertEqual(SensorValue.objects.filter(
            sensor__value_id='shop5/section1&4/temperature/regular').count(), 2)
        self.assertEqual(SensorValue.objects.filter(
            sensor__value_id='shop5/section2&3/temperature/regular').count(), 2)
        self.assertEqual(SensorValue.objects.filter(
            sensor__value_id='shop5/section1/counter/regular').count(), 1)