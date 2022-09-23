from geopy.geocoders import Nominatim
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
geolocator = Nominatim(user_agent="geotest")


def get_weather_data(location):
    location = geolocator.geocode(location)
    print(location.address)
    latitude = "%.2f" % location.latitude
    longitude = "%.2f" % location.longitude
    http = requests.Session()

    # Mount it for both http and https usage
    # adapter = HTTPAdapter()

    http.mount("https://", adapter)
    http.mount("http://", adapter)
    start_date = "2022-09-23"
    end_date = "2022-09-29"
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
    weather_time_list = []

    for i in range(7):
        for j in range(168):
            weather_times = {
                hourly_data['time'][j][11:13]: {
                    'temp': hourly_data['temperature_2m'][j],
                    'cloudcover': hourly_data['cloudcover'][j],
                    'precipitation': hourly_data['precipitation'][j],
                    'snowfall': hourly_data['snowfall'][j],
                    'weathercode': hourly_data['weathercode'][j],

                }
            }
            weather_time_list.append(weather_times)

    # chunk weather_time_list to put into daily data
        our_list = weather_time_list
        chunk_size = 24
        chunked_list = [our_list[i:i + chunk_size] for i in range(0, len(our_list), chunk_size)]

        daily_weather_data = {
            daily_data['time'][i]: {
                    'temp_max': daily_data['temperature_2m_max'][i],
                    'temp_min': daily_data['temperature_2m_min'][i],
                    'precipitation_sum': daily_data['precipitation_sum'][i],
                    'snowfall_sum': daily_data['snowfall_sum'][i],
                    'temp_current': current_data['temperature'],
                    'weather_times': chunked_list[i]
            }
        }
        print(daily_weather_data)


get_weather_data('seoul')
