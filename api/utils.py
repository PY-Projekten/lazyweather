from geopy.geocoders import Nominatim
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import numpy as np
import pandas as pd

retry_strategy = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)

geolocator = Nominatim(user_agent="geotest")


# Huebbesweg 32, 20537 Hamburg Germany


def latitude_longitude(location):
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
        f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&current_weather=True&hourly=temperature_2m,cloudcover&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum&timezone=Europe%2FBerlin')
    data = r.json()



    data_current = data['current_weather']
    data_hourly = data['hourly']
    data_daily = data['daily']


    weather_time_list = []

    # for j in range(168):
    #     weather_times = {
    #         data_hourly['time'][j][11:13]: {
    #             'temp': data_hourly['temperature_2m'][j],
    #             'cloudcover': data_hourly['cloudcover'][j],
    #
    #         }
    #     }
    #     print(weather_times)

    for i in range(7):
        for j in range(168):
            weather_times = {
                data_hourly['time'][j][11:13]: {
                    'temp': data_hourly['temperature_2m'][j],
                    'cloudcover': data_hourly['cloudcover'][j],

                }
            }
            weather_time_list.append(weather_times)
        #print(weather_time_list)
        our_list = weather_time_list

        chunk_size = 24
        chunked_list = [our_list[i:i + chunk_size] for i in range(0, len(our_list), chunk_size)]

        #print(chunked_list)

        new_weather_data = {
            data_daily['time'][i]: {
                    'temp_max': data_daily['temperature_2m_max'][i],
                    'temp_min': data_daily['temperature_2m_min'][i],
                    'precipitation_sum': data_daily['precipitation_sum'][i],
                    'snowfall_sum': data_daily['snowfall_sum'][i],
                    'temp_current': data_current['temperature'],
                    'weather_times': chunked_list[i]
            }
        }
        print(new_weather_data)





    '''
    # temporary unused

    weather_data = {
        'current': {'time': data_current['time'], 'temperature': data_current['temperature']},
        'hourly': {'time': data_hourly['time'], 'temperature': data_hourly['temperature_2m'],
                   'cloudcover': data_hourly['cloudcover']},
        'daily': {'time': data_daily['time'], 'max_temperature': data_daily['temperature_2m_max'],
                  'min_temperature': data_daily['temperature_2m_min'],
                  'precipitation_sum': data_daily['precipitation_sum'], 'snowfall_sum': data_daily['snowfall_sum']}
    }
    '''

    '''
    # Übung gemacht mit Pandas
    '''

    '''
    print(weather_data)
    c_df = pd.DataFrame(weather_data['current'], index=[0])
    h_df = pd.DataFrame(weather_data['hourly'])
    d_df = pd.DataFrame(weather_data['daily'])
    df = pd.to_datetime(weather_data['hourly']['time'])
    print(df)
    print(c_df)
    print(h_df)
    print(d_df)
    '''


latitude_longitude('Huebbesweg 32, 20537 Hamburg Germany')
