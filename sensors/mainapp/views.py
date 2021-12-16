# -*- coding: utf-8 -*-
import datetime
from django.db import models
from rest_framework import status, views, serializers, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django_filters import rest_framework as filters

from mainapp.models import Workshop, Location, Sensor, SensorValue
from mainapp import selectors



class TempDeviationsView(views.APIView):
    # authentication_classes = [JSONWebTokenAuthentication]
    # permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        d1 = serializers.DateField()
        d2 = serializers.DateField()
        t_min = serializers.FloatField()
        t_max = serializers.FloatField()


    class WorkshopSerializer(serializers.ModelSerializer):

        class LocationSerializer(serializers.ModelSerializer):

            class SensorSerializer(serializers.ModelSerializer):
                count_deviations_lt_t_min = serializers.ReadOnlyField()
                count_deviations_gt_t_max = serializers.ReadOnlyField()
                count_all_values = serializers.ReadOnlyField()
                # count_all_deviations = serializers.ReadOnlyField()
                # deviations_per_cent = serializers.ReadOnlyField()

                class Meta:
                    model = Sensor
                    fields = ['name', 'count_deviations_lt_t_min', 'count_deviations_gt_t_max',
                        'count_all_values', 'id',  ]

            sensors = SensorSerializer(many=True)

            class Meta:
                model = Location
                fields = ['section_number', 'sensors']

        locations = LocationSerializer(many=True)

        class Meta:
            model = Workshop
            fields = ['ws_number', 'locations']


    def get(self, request, format=None):
        serializer = self.InputSerializer(data=request.GET)

        if serializer.is_valid():
            workshops = selectors.get_temp_deviations_by_workshops(
                t_min=serializer.validated_data['t_min'],
                t_max=serializer.validated_data['t_max'],
                d1=serializer.validated_data['d1'],
                d2=serializer.validated_data['d2'])

            data = dict()
            for ws in self.WorkshopSerializer(workshops, many=True).data:
                data[f"ws_{ws['ws_number']}"] = ws

            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorValuesListView(generics.ListAPIView):

    class SensorValueReadSerializer(serializers.ModelSerializer):
        date_ts = serializers.ReadOnlyField()

        class Meta:
            model = SensorValue
            fields = ['value', 'date_ts']


    class SensorValueFilter(filters.FilterSet):
        value_gt = filters.NumberFilter(field_name="value", lookup_expr='gt')
        value_lt = filters.NumberFilter(field_name="value", lookup_expr='lt')

        deviations = filters.RangeFilter(method='filter_deviations')
        daterange = filters.DateFromToRangeFilter(method='filter_daterange')

        def filter_deviations(self, queryset, name, value):
            value = (value.start, value.stop)
            return queryset.filter(models.Q(value__lt=value[0]) | models.Q(value__gt=value[1]))

        def filter_daterange(self, queryset, name, date_range):
            date_range = (date_range.start, date_range.stop)
            return queryset.filter(date__date__gte=date_range[0], date__date__lte=date_range[1])

        class Meta:
            model = SensorValue
            fields = '__all__'


    class LargeResultsSetPagination(PageNumberPagination):
        page_size = 1000
        page_size_query_param = 'page_size'
        max_page_size = 10000


    queryset = SensorValue.objects.all()
    serializer_class = SensorValueReadSerializer
    # permission_classes = [IsAuthenticated, CanSeeRamaStockPermissions]
    filter_class = SensorValueFilter
    pagination_class = LargeResultsSetPagination