from django.urls import path, re_path
from django.conf.urls import include
from .views import location_list, location_detail, weather_list, weather_detail
from api.views import get_weather
from .views import weather_list, weather_display

urlpatterns = [
    path('location/', location_list),
    re_path('location/(?P<pk>[0-9]+)/$', location_detail),
    path('weather-data/', weather_list),
    re_path('weather-data/(?P<pk>[0-9]+)/$', weather_detail),
    path('weather/display/', weather_display, name='weather_display'),
]
