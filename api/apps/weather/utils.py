from geopy.geocoders import Nominatim
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
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


# def get_weather_data(location, days=7):
#     print("get_weather_data function called")
#     """
#     Return daily weather data from open-meteo.com starting today
#     Receive the location as a parameter and returns the weather of it
#     :param location: Address
#     :param days: Number of days(max = 7)
#     :return: Daily weather data in list form
#     """
#     geoloc = geolocator.geocode(location)
#     address = None
#     #if location:
#     #    address = location.address
#     #    print(location.address)
#     latitude = "%.2f" % geoloc.latitude
#     longitude = "%.2f" % geoloc.longitude
#     db_location = Location.objects.filter(longitude=longitude, latitude=latitude).first()
#
#     if db_location is None:
#         db_location = Location.objects.create(longitude=longitude, latitude=latitude, name=location.lower())
#     # try:
#     #
#     #
#     #
#     # except:
#     #     location = Location.objects.create(longitude=longitude, latitude=latitude)
#     #     location.save()
#
#     print(location)
#     qr = []
#     try:
#         date = django.utils.timezone.now()
#         data = WeatherData.objects.filter(location=db_location.id, date=date).first()
#         if data is not None:
#             print('from database', data.data)
#             qr = data.data
#
#         print('from API')
#         http = requests.Session()
#
#         # Mount it for both http and https usage
#         # adapter = HTTPAdapter()
#
#         http.mount("https://", adapter)
#         http.mount("https://", adapter)
#         start_date = datetime.date.today()
#         end_date = datetime.date.today() + datetime.timedelta(days)
#         # Debugging of API request
#         print("Before API request")
#         r = http.get(
#             f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}'
#             f'&start_date={start_date}&end_date={end_date}'
#             f'&current_weather=True'
#             f'&hourly=temperature_2m,precipitation,snowfall,weathercode,cloudcover'
#             f'&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum&timezone=Europe%2FBerlin')
#         print("After API request")
#         # Printing the raw JSON response from the API
#         print(f"API Response: {r.json()}")
#         data = r.json()
#         current_data = data['current_weather']
#         hourly_data = data['hourly']
#         daily_data = data['daily']
#         daily_weather_data_list = []
#         hours = 24
#         for i in range(days):
#             weather_times = {}
#             offset = i * hours
#             for j in range(hours):
#                 w_code = hourly_data['weathercode'][j + offset]
#                 icon = get_icon_by_weathercode(w_code)
#                 weather_times[hourly_data['time'][j][11:13]] = {
#                     'temp': hourly_data['temperature_2m'][j + offset],
#                     'cloudcover': hourly_data['cloudcover'][j + offset],
#                     'precipitation': hourly_data['precipitation'][j + offset],
#                     'snowfall': hourly_data['snowfall'][j + offset],
#                     'weathercode': w_code,
#                     'weather_icon': icon,
#
#                 }
#             # Save each day’s data to the database here
#             WeatherData.objects.create(location=db_location, data=daily_weather_data_list[i], date=daily_data['time'][i])
#
#             daily_weather_data = {
#                 daily_data['time'][i]: {
#                     'temp_max': daily_data['temperature_2m_max'][i],
#                     'temp_min': daily_data['temperature_2m_min'][i],
#                     'precipitation_sum': daily_data['precipitation_sum'][i],
#                     'snowfall_sum': daily_data['snowfall_sum'][i],
#                     'temp_current': current_data['temperature'],
#                     'weather_times': weather_times
#                 }
#             }
#
#             daily_weather_data_list.append(daily_weather_data)
#         WeatherData.objects.create(location=db_location, data=daily_weather_data_list)
#         qr = daily_weather_data_list
#     except Exception as e:
#         print(e)
#     return qr
# #Ruhrstraße 46-88, 22761 Hamburg
#
# if __name__ == '__main__':
#     get_weather_data('berlin')



# Version: Updating existing records (new dates for locations; current dates)
def get_weather_data(location, days=7):
    print("get_weather_data function called")
    """
    Return daily weather data from open-meteo.com starting today.
    Receive the location as a parameter and returns the weather of it.
    :param location: Address
    :param days: Number of days(max = 7)
    :return: Daily weather data in list form
    """
    geoloc = geolocator.geocode(location)
    latitude = "%.2f" % geoloc.latitude
    longitude = "%.2f" % geoloc.longitude
    db_location = Location.objects.filter(longitude=longitude, latitude=latitude).first()

    # Check if the location already exists in the database
    if db_location is None:
        db_location = Location.objects.create(longitude=longitude, latitude=latitude, name=location.lower())

    # Check if the weather data for the location is up-to-date
    date = django.utils.timezone.now()
    data = WeatherData.objects.filter(location=db_location.id, date=date).first()
    if data is not None:
        print('Data retrieved from database', data.data)
        return data.data  # Return the data from the database if it's up-to-date

    # If data is not in the database, fetch it from the API
    qr = []  # Initialize the query result variable
    try:
        print('Data retrieved from API')
        http = requests.Session()
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

        # Modification 3: Save all the days' data to the database at once
        WeatherData.objects.create(location=db_location, data=daily_weather_data_list, date=date)

        qr = daily_weather_data_list  # Assign the processed data to qr

    except Exception as e:
        print(e)
    return qr
#Ruhrstraße 46-88, 22761 Hamburg

if __name__ == '__main__':
    get_weather_data('berlin')

