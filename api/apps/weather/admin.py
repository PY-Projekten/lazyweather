from django.contrib import admin

from api.apps.weather.models import Location
from api.apps.weather.models import WeatherData

admin.site.register(Location)
admin.site.register(WeatherData)

