# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils import timezone

from core.models import CoreModel


class Workshop(CoreModel):
    ws_number = models.IntegerField()

    def __str__(self):
        return f'Ws {self.ws_number}'


class LocationQuerySet(models.QuerySet):
    pass


class Location(CoreModel):
    workshop = models.ForeignKey(Workshop, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='locations')
    ws_number = models.IntegerField(null=True, blank=True)
    section_number = models.IntegerField(null=True, blank=True)
    out_ws_name = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)

    objects = LocationQuerySet.as_manager()

    def __str__(self):
        return self.name


class SensorQuerySet(models.QuerySet):
    pass


class Sensor(CoreModel):
    SENSOR_TYPES = [('temp', 'temp'), ('elec', 'elec'), ('water', 'water'), ('pressure', 'pressure')]
    sensor_type = models.CharField(max_length=50, choices=SENSOR_TYPES)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sensors')

    value_id = models.CharField(max_length=100)
    value_key = models.CharField(max_length=50, default='')

    name = models.CharField(max_length=100, default='')

    active = models.BooleanField(default=True)

    objects = SensorQuerySet.as_manager()

    def __str__(self):
        return f'Sensor {self.sensor_type} {self.location} {self.name}'


class SensorValueQuerySet(models.QuerySet):
    pass


class SensorValue(CoreModel):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='values')
    value = models.FloatField()
    date = models.DateTimeField()

    objects = SensorValueQuerySet.as_manager()

    class Meta:
        unique_together = [['sensor', 'date']]

    def __str__(self):
        return f'{self.date} {self.sensor} {self.value}'

    @property
    def date_ts(self):
        return datetime.datetime.timestamp(self.date) * 1000

