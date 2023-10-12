from django.db import models
from django.db.models.deletion import CASCADE
import django.utils.timezone


class Location(models.Model):
    """"""
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Location'
        unique_together = ('longitude', 'latitude')
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        if self.name:
            return self.name
        return f'{self.longitude}-{self.latitude}'

    def __repr__(self):
        return self.name


class WeatherData(models.Model):
    """"""
    location = models.ForeignKey(Location, on_delete=CASCADE)
    data = models.JSONField(default=dict)
    date = models.DateField(default=django.utils.timezone.now)

    class Meta:
        db_table = 'weather_data'
        unique_together = ('location', 'data', 'date')
        verbose_name = 'Weather Data'
        verbose_name_plural = 'Weather Datas'
    def  __str__(self):
        return self.location.name