from geopy.geocoders import Nominatim
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import datetime

retry_strategy = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
geolocator = Nominatim(user_agent="geotest")

# WEATHER_DESCRIPTION = {
#     0: "Clear sky",
#     1: "Mainly clear",
#     2: "partly cloudy",
#     3: "overcast",
#     45: "Fog",
#     48: "depositing rime fog",
#     51: "Drizzle: Light",
#     53: "Drizzle: moderate",
#     55: "Drizzle: dense intensity",
#     56: "Freezing Drizzle: Light",
#     57: "Freezing Drizzle: dense intensity",
#     61: "Rain: Slight",
#     63: "Rain: moderate",
#     65: "Rain: heavy intensity",
#     66: "Freezing Rain: Light",
#     67: "Freezing Rain: heavy intensity",
#     71: "Snow fall: Slight",
#     73: "Snow fall: moderate",
#     75: "Snow fall: heavy intensity",
#     77: "Snow grains",
#     80: "Rain showers: Slight",
#     81: "Rain showers: moderate",
#     82: "Rain showers: violent",
#     85: "Snow showers slight",
#     86: "Snow showers heavy",
#     95: "Thunderstorm: Slight or moderate",
#     96: "Thunderstorm with slight",
#     99: "Thunderstorm with heavy hail"
# }

WEATHER_DESCRIPTION = {
    0: "Sonne",
    1: "Sonne",
    2: "Sonne hinter kleiner Wolke",
    3: "Sonne hinter großer Wolke",
    45: "Nebel",
    48: "Nebel",
    51: "Sonne mit heller Regenwolke und wenig Regen",
    53: "Sonne mit heller Regenwolke und wenig Regen",
    55: "Sonne mit dunkler Regenwolke und wenig Regen",
    56: "Sonne mit heller Regenwolke und wenig Regen",
    57: "Sonne mit dunkler Regenwolke und wenig Regen",
    61: "Sonne mit heller Regenwolke und wenig Regen",
    63: "Sonne mit heller Regenwolke und wenig Regen",
    65: "Sonne mit dunkler Regenwolke und wenig Regen",
    66: "Sonne mit heller Regenwolke und wenig Regen",
    67: "Sonne mit dunkler Regenwolke und wenig Regen",
    71: "Regenwolke",
    73: "Regenwolke",
    75: "Regenwolke",
    77: "Regenwolke",
    80: "Sonne mit heller Regenwolke und wenig Regen",
    81: "Sonne mit heller Regenwolke und wenig Regen",
    82: "Sonne mit dunkler Regenwolke und wenig Regen",
    85: "Regenwolke",
    86: "Regenwolke",
    95: "Mond",
    96: "Mond",
    99: "Mond"
}

WEATHER_ICONS = {
    "Sonne hinter großer Wolke": {"icon": "mdi-weather-cloudy", "color": "grey", "description": "Bewölkt"},
    "Helle Wolke": {"icon": "mdi-weather-cloudy", "color": "lightgrey", "description": "Bewölkt"},

    "Mond hinter großer Wolke": {"icon": "mdi-weather-cloudy", "color": "grey", "description": "Bewölkt"},

    "Kleine Sonne mit dunkler Wolke": {"icon": "mdi-weather-cloudy", "color": "grey", "description": "Bewölkt"},
    "Sonne hinter kleiner Wolke": {"icon": "mdi-weather-partly-cloudy", "color": "lightgrey",
                                   "description": "Leicht Bewölkt"},

    "Dunkle Wolke mit wenig Regen": {"icon": "mdi-weather-partly-rainy", "color": "darkblue",
                                     "description": "Leichter Regen"},
    "Sonne mit dunkler Regenwolke und wenig Regen": {"icon": "mdi-weather-partly-rainy", "color": "grey",
                                                     "description": "Leichter Regen"},
    "Sonne mit heller Regenwolke und wenig Regen": {"icon": "mdi-weather-partly-rainy", "color": "lightgrey",
                                                    "description": "Leichter Regen"},
    "Mond mit dunkler Regenwolke und wenig Regen": {"icon": "mdi-weather-partly-rainy", "color": "grey",
                                                    "description": "Leichter Regen"},
    "Mond mit heller Regenwolke und wenig Regen": {"icon": "mdi-weather-partly-rainy", "color": "lightgrey",
                                                   "description": "Leichter Regen"},
    "Sonne mit Regenwolke": {"icon": "mdi-weather-partly-rainy", "color": "lightblue", "description": "Regen"},
    "Regenwolke": {"icon": "mdi-weather-rainy", "color": "blue", "description": "Regen"},

    "Mond hinter kleiner Wolke": {"icon": "mdi-eather-night-partly-cloudy", "color": "lightgrey",
                                  "description": "Leicht Bewölkt"},
    "Kleiner Mond mit dunkler Wolke": {"icon": "mdi-weather-night-partly-cloudy", "color": "grey",
                                       "description": "Bewölkt"},
    "Mond": {"icon": "mdi-weather-night", "color": "grey", "description": "Klar"},

    "Sonne": {"icon": "mdi-weather-sunny", "color": "yellow", "description": "Klar"},
    "Sonnenaufgang": {"icon": "mdi-weather-sunny", "color": "yellow", "description": "Klar"},
    "Sonnenuntergang": {"icon": "mdi-weather-sunny", "color": "yellow", "description": "Klar"},

    "Nebel": {"icon": "mdi-weather-fog", "color": "grey", "description": "Nebel"}
}


def get_icon_by_weathercode(weathercode):
    weather_description = WEATHER_DESCRIPTION[weathercode]
    print(WEATHER_ICONS[weather_description])


def get_weather_data(location, days=7):
    location = geolocator.geocode(location)
    print(location.address)
    latitude = "%.2f" % location.latitude
    longitude = "%.2f" % location.longitude
    http = requests.Session()

    # Mount it for both http and https usage
    # adapter = HTTPAdapter()

    http.mount("https://", adapter)
    http.mount("http://", adapter)
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

    hours = 24
    for i in range(days):
        weather_times = {}
        offset = i * hours
        for j in range(hours):
            weather_times[hourly_data['time'][j][11:13]] = {
                    'temp': hourly_data['temperature_2m'][j + offset],
                    'cloudcover': hourly_data['cloudcover'][j + offset],
                    'precipitation': hourly_data['precipitation'][j + offset],
                    'snowfall': hourly_data['snowfall'][j + offset],
                    'weathercode': hourly_data['weathercode'][j + offset],

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

        print(daily_weather_data)


get_weather_data('berlin')
