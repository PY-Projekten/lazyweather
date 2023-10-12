# Lazyweather

<br>

## Beschreibung

Die Lazyweather-API ist eine Python API, welche sich Wetterdaten von der [open-meteo.com](https://open-meteo.com/en) Webseite bezieht. Lazyweather API gibt die Wetterdaten wie Temperaturen, Windgeschwindigkeiten, Feuchtigkeiten und viele andere Daten zurück.

## API-Views

* get_weather

| Method | Url                          | Parameter          | Erklärung                   |
|--------|------------------------------|--------------------|-----------------------------|
| GET    | /api/v1/weather/[location]   | location : Adresse | Abrufen von Witterungsdaten |

* location_list

| Method | Url              | Erklärung           |
|--------|------------------|---------------------|
| GET    | /api/v1/location | Abrufen eines Orts  |
| POST   |                  | Anlegen eines Orts  |  

* location_detail

| Method | Url                   | Parameter        | Erklärung                |
|--------|-----------------------|------------------|--------------------------|
| GET    | /api/v1/location/[pk] | pk : Primary Key | Abrufen eines Orts       |
| PUT    |                       |                  | Aktualisieren eines Orts |
| PATCH  |                       |                  | Aktualisieren eines Orts | 
| DELETE |                       |                  | Löschen eines Orts       |

* weather_list

| Method | Url                   | Erklärung                              |
|--------|-----------------------|----------------------------------------|
| GET    | /api/v1/weather-data  | Abrufen von täglichen Witterungsdaten  |
| POST   |                       | Anlegen von täglichen Witterungsdaten  |

* weather_detail

| Method  | Url                       | Parameter        | Erklärung                                   |
|---------|---------------------------|------------------|---------------------------------------------|
| GET     | /api/v1/weather-data/[pk] | pk : Primary Key | Abrufen von täglichen Witterungsdaten       |
| PUT     |                           |                  | Aktualisieren von täglichen Witterungsdaten |
| PATCH   |                           |                  | Aktualisieren von täglichen Witterungsdaten |
| DELETE  |                           |                  | Löschen von täglichen Witterungsdaten       |

