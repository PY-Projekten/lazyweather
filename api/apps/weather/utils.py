from geopy.geocoders import Nominatim
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import datetime
from api.config import *
from api.apps.weather.serializers import LocationSerializer, WeatherDataSerializer
from .models import Location, WeatherData
import django.utils.timezone
from rest_framework import serializers

retry_strategy = Retry(
    total=10,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
geolocator = Nominatim(user_agent="test", timeout=5)


def get_icon_by_weathercode(weathercode):
    """
    Get the weather codes from config.py and match them to the weather icons
    :param weathercode: Weather codes
    :return: Weather icons in dictionary form
    """

    weather_description = WEATHER_DESCRIPTION[weathercode]
    return WEATHER_ICONS[weather_description]


def get_weather_data(location, days=7):
    """
    Return daily weather data from open-meteo.com starting today
    Receive the location as a parameter and returns the weather of it
    :param location: Address
    :param days: Number of days(max = 7)
    :return: Daily weather data in list form
    """
    location = geolocator.geocode(location)
    address = None
    if location:
        address = location.address
        print(location.address)
    latitude = "%.2f" % location.latitude
    longitude = "%.2f" % location.longitude
    location = Location.objects.filter(longitude=longitude, latitude=latitude).first()

    if location is None:
        location = Location.objects.create(longitude=longitude, latitude=latitude, name=address)
    # try:
    #
    #
    #
    # except:
    #     location = Location.objects.create(longitude=longitude, latitude=latitude)
    #     location.save()

    print(location)

    try:
        date = django.utils.timezone.now()
        data = WeatherData.objects.filter(location=location, date=date).first()
        if data is not None:
            print('from database')
            return data.data

        print('from API')
        http = requests.Session()

        # Mount it for both http and https usage
        # adapter = HTTPAdapter()

        http.mount("https://", adapter)
        http.mount("https://", adapter)
        start_date = datetime.date.today()
        end_date = datetime.date.today() + datetime.timedelta(days)
        r = http.get(
            f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}'
            f'&start_date={start_date}&end_date={end_date}'
            f'&current_weather=True'
            f'&hourly=temperature_2m,precipitation,snowfall,weathercode,cloudcover'
            f'&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum&timezone=Europe%2FBerlin')
        data = r.json()
        current_data = data['current_weather']
        hourly_data = data['hourly']
        daily_data = data['daily']
        daily_weather_data_list = []
        hours = 24
        for i in range(days):
            weather_times = {}
            offset = i * hours
            for j in range(hours):
                w_code = hourly_data['weathercode'][j + offset]
                icon = get_icon_by_weathercode(w_code)
                weather_times[hourly_data['time'][j][11:13]] = {
                    'temp': hourly_data['temperature_2m'][j + offset],
                    'cloudcover': hourly_data['cloudcover'][j + offset],
                    'precipitation': hourly_data['precipitation'][j + offset],
                    'snowfall': hourly_data['snowfall'][j + offset],
                    'weathercode': w_code,
                    'weather_icon': icon,

                }

            daily_weather_data = {
                daily_data['time'][i]: {
                    'temp_max': daily_data['temperature_2m_max'][i],
                    'temp_min': daily_data['temperature_2m_min'][i],
                    'precipitation_sum': daily_data['precipitation_sum'][i],
                    'snowfall_sum': daily_data['snowfall_sum'][i],
                    'temp_current': current_data['temperature'],
                    'weather_times': weather_times
                }
            }

            daily_weather_data_list.append(daily_weather_data)
        WeatherData.objects.create(location=location, data=daily_weather_data_list)
        return daily_weather_data_list
    except Exception as e:
        print(e)
#Ruhrstraße 46-88, 22761 Hamburg

if __name__ == '__main__':
    get_weather_data('berlin')