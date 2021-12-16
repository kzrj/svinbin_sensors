# -*- coding: utf-8 -*-
import datetime

from django.db.models import Q, Prefetch, OuterRef, Subquery, Count, F, Case, When, \
    ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce

from mainapp.models import Sensor, SensorValue, Workshop, Location


def get_temp_deviations_count_by_sensors(t_min, t_max, d1, d2):
    values_qs = SensorValue.objects.filter(sensor__pk=OuterRef('pk')) \
        .filter(date__date__gte=d1, date__date__lte=d2)

    subquery_t_min = values_qs.filter(value__lt=t_min) \
        .values('sensor') \
        .annotate(count=Count('pk')) \
        .values('count')

    subquery_t_max = values_qs.filter(value__gt=t_max) \
        .values('sensor') \
        .annotate(count=Count('pk')) \
        .values('count')

    subquery_count_all = values_qs \
                            .values('sensor') \
                            .annotate(count=Count('pk')) \
                            .values('count')

    return Sensor.objects.filter(sensor_type='temp') \
            .annotate(count_deviations_lt_t_min=Coalesce(Subquery(subquery_t_min), 0),
                      count_deviations_gt_t_max=Coalesce(Subquery(subquery_t_max), 0),
                      count_all_values=Coalesce(Subquery(subquery_count_all), 0))
            # .annotate(count_all_deviations=F('count_deviations_lt_t_min') + F('count_deviations_gt_t_max')) \
            # .annotate(deviations_per_cent=Case(
            #         When(count_all_values=0.0, then=0.0),
            #         When(count_all_values__gt=0, 
            #                 then=ExpressionWrapper(
            #                     F('count_all_deviations') * 100.0 / F('count_all_values'),
            #                     output_field=FloatField())
            #             ), output_field=FloatField()
            #         )
            # )
                


def get_temp_deviations_by_workshops(**kwargs):
    return Workshop.objects.exclude(ws_number=99).prefetch_related(
        Prefetch(
            'locations',
            queryset=Location.objects.all().prefetch_related(
                Prefetch(
                    'sensors',
                    queryset=get_temp_deviations_count_by_sensors(**kwargs)
                    )
                ),
            )
        )