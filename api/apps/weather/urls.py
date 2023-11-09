from django.urls import path, re_path
from django.conf.urls import include
from .views import location_list, location_detail, weather_list, weather_detail#, weather_q
from api.views import get_weather
from .views import weather_list, weather_display, weather_query, get_weather_by_location, available_locations

urlpatterns = [
    path('location/', location_list),
    re_path('location/(?P<pk>[0-9]+)/$', location_detail),
    path('weather-data/', weather_list),
    re_path('weather-data/(?P<pk>[0-9]+)/$', weather_detail),
    re_path('weather-data/(?P<location>\w+)/$', get_weather_by_location),
    path('weather/display/', weather_display, name='weather_display'),
    path('weather_query/', weather_query, name='weather_query'),
    re_path(r'get/weather/(?P<location>[a-zA-Z]+)/$', get_weather, name='weather_query'),
    path('available_locations/', available_locations, name='available_locations'),
    #path('weather_q/', weather_q, name='weather_q'),
]
