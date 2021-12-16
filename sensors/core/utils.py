# -*- coding: utf-8 -*-
from mainapp.models import Location, Sensor, Workshop


def init_locations():
    Workshop.objects.bulk_create(
        [
            Workshop(ws_number=1), Workshop(ws_number=2), Workshop(ws_number=3), Workshop(ws_number=4),
            Workshop(ws_number=5), Workshop(ws_number=6), Workshop(ws_number=7), Workshop(ws_number=8),
            Workshop(ws_number=99)
        ]
    )

    ws1 = Workshop.objects.get(ws_number=1)
    ws2 = Workshop.objects.get(ws_number=2)
    ws3 = Workshop.objects.get(ws_number=3)
    ws4 = Workshop.objects.get(ws_number=4)
    ws5 = Workshop.objects.get(ws_number=5)
    ws6 = Workshop.objects.get(ws_number=6)
    ws7 = Workshop.objects.get(ws_number=7)
    ws8 = Workshop.objects.get(ws_number=8)
    out_ws = Workshop.objects.get(ws_number=99)

    Location.objects.create(ws_number=1, name='Цех 1', workshop=ws1)
    Location.objects.create(ws_number=2, name='Цех 2', workshop=ws2)

    Location.objects.create(ws_number=3, name='Цех 3', workshop=ws3)
    for i in range(1, 7):
        Location.objects.create(ws_number=3, section_number=i, name=f'Цех 3 секция {i}',
            workshop=ws3)

    Location.objects.create(ws_number=4, name='Цех 4', workshop=ws4)
    for i in range(1, 11):
        Location.objects.create(ws_number=4, section_number=i, name=f'Цех 4 секция {i}',
            workshop=ws4)

    Location.objects.create(ws_number=8, name='Цех 8', workshop=ws8)
    for i in range(1, 5):
        Location.objects.create(ws_number=8, section_number=i, name=f'Цех 8 секция {i}', 
            workshop=ws8)

    Location.objects.create(ws_number=5, name='Цех 5', workshop=ws5)
    for i in range(1, 5):
        Location.objects.create(ws_number=5, section_number=i, name=f'Цех 5 секция {i}',
            workshop=ws5)

    Location.objects.create(ws_number=6, name='Цех 6', workshop=ws6)
    for i in range(1, 5):
        Location.objects.create(ws_number=6, section_number=i, name=f'Цех 6 секция {i}',
            workshop=ws6)

    Location.objects.create(ws_number=7, name='Цех 7', workshop=ws7)
    for i in range(1, 6):
        Location.objects.create(ws_number=7, section_number=i, name=f'Цех 7 секция {i}',
            workshop=ws7)

    Location.objects.create(out_ws_name='boiler', name='Котельная', workshop=out_ws)
    Location.objects.create(out_ws_name='pumps', name='Насосная', workshop=out_ws)

def init_sensors_ws1_ws2():
    ws1 = Location.objects.get(ws_number=1, name='Цех 1')
    Sensor.objects.create(sensor_type='temp', location=ws1, value_key='temperature',
        value_id='shop1/pair1/temperature/regular')
    Sensor.objects.create(sensor_type='temp', location=ws1, value_key='temperature',
        value_id='shop1/pair2/temperature/regular')
    Sensor.objects.create(sensor_type='elec', location=ws1, value_key='rate',
        value_id='shop1/electro/regular')
    Sensor.objects.create(sensor_type='water', location=ws1, value_key='consumption',
        value_id='shop2/watercounter/regular')

    ws2 = Location.objects.get(ws_number=2, name='Цех 2')
    Sensor.objects.create(sensor_type='temp', location=ws2, value_key='temperature',
        value_id='shop2/pair1/temperature/regular')
    Sensor.objects.create(sensor_type='temp', location=ws2, value_key='temperature',
        value_id='shop2/pair2/temperature/regular')
    Sensor.objects.create(sensor_type='elec', location=ws2, value_key='rate',
        value_id='shop2/electro/regular')
    Sensor.objects.create(sensor_type='water', location=ws2, value_key='consumption',
        value_id='shop2/watercounter/regular')


def init_sensors_ws3_ws4_ws8(ws_number):
    ws = Location.objects.get(ws_number=ws_number, name=f'Цех {ws_number}')
    Sensor.objects.create(sensor_type='elec', location=ws, value_key='rate',
        value_id=f'shop{ws_number}/electro/regular')
    Sensor.objects.create(sensor_type='water', location=ws, value_key='consumption',
        value_id=f'shop{ws_number}/watercounter/regular')

    for ws_sec in Location.objects.filter(ws_number=ws_number, section_number__isnull=False):
        Sensor.objects.create(sensor_type='temp', location=ws_sec, value_key='temperature',
            value_id=f'shop{ws_sec.ws_number}/section{ws_sec.section_number}/temperature/regular')


def init_sensors_ws_otkorm(ws_number):
    ws = Location.objects.get(ws_number=ws_number, name=f'Цех {ws_number}')
    Sensor.objects.create(sensor_type='elec', location=ws, value_key='rate',
        value_id=f'shop{ws_number}/electro/regular')

    for ws_sec in Location.objects.filter(ws_number=ws_number, section_number__isnull=False):
        if ws_sec.ws_number == 7:
            Sensor.objects.create(sensor_type='temp', location=ws_sec, value_key='temperature',
                value_id=f'shop{ws_sec.ws_number}/section{ws_sec.section_number}/temperature/regular')
        else:
            if ws_sec.section_number in [1, 4]:
                 Sensor.objects.create(sensor_type='temp', location=ws_sec, value_key='temperature',
                    value_id=f'shop{ws_sec.ws_number}/section1&4/temperature/regular')
            if ws_sec.section_number in [2, 3]:
                 Sensor.objects.create(sensor_type='temp', location=ws_sec, value_key='temperature',
                    value_id=f'shop{ws_sec.ws_number}/section2&3/temperature/regular')

        Sensor.objects.create(sensor_type='water', location=ws_sec, value_key='consumption',
            value_id=f'shop{ws_sec.ws_number}/section{ws_sec.section_number}/counter/regular')


def init_sensors_rest():
    pupms = Location.objects.get(out_ws_name='pumps')
    Sensor.objects.create(sensor_type='pressure', location=pupms, value_id='pumps/water/pressure',
        name='Давление', value_key='pressure')
    Sensor.objects.create(sensor_type='temp', location=pupms, value_id='pumps/house',
        value_key='outsidetemperature', name='Температура на улице')
    Sensor.objects.create(sensor_type='temp', location=pupms, value_id='pumps/house',
        value_key='insidetemperature', name='Температура внутри')
    Sensor.objects.create(sensor_type='water', location=pupms, value_id='pumps/common/watercounter/regular',
        value_key='consumption', name='Общее потребление')
    Sensor.objects.create(sensor_type='water', location=pupms, value_id='pumps/well/watercounter/regular',
        value_key='consumption', name='Well water')
    Sensor.objects.create(sensor_type='water', location=pupms, value_id='pumps/ecofood/watercounter/regular',
        value_key='consumption', name='Расход экофуд')
    Sensor.objects.create(sensor_type='elec', location=pupms, value_id='',
        value_key='', name='Электричество')

    boiler = Location.objects.get(out_ws_name='boiler')
    Sensor.objects.create(sensor_type='temp', location=boiler, value_id='boiler/regular',
        value_key='supplytemperature1', name='Подача 1')
    Sensor.objects.create(sensor_type='temp', location=boiler, value_id='boiler/regular',
        value_key='supplytemperature2', name='Подача 2')
    Sensor.objects.create(sensor_type='temp', location=boiler, value_id='boiler/regular',
        value_key='mixtemperature', name='Смешанная')
    Sensor.objects.create(sensor_type='temp', location=boiler, value_id='boiler/regular',
        value_key='returntemperature', name='Отработка')
    Sensor.objects.create(sensor_type='water', location=boiler, value_id='boiler/watercounter/regular',
        value_key='consumption', name='Потребление')

def init_sensors():
    init_sensors_ws1_ws2()

    for i in [3, 4, 8]:
        init_sensors_ws3_ws4_ws8(ws_number=i)

    for i in [5, 6, 7]:
        init_sensors_ws_otkorm(ws_number=i)

    init_sensors_rest()