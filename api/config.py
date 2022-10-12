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