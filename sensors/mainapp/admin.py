from django.contrib import admin

from mainapp.models import Location, Sensor, SensorValue, Workshop


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Location._meta.fields]


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Sensor._meta.fields]


@admin.register(SensorValue)
class SensorValueAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SensorValue._meta.fields]


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Workshop._meta.fields]
