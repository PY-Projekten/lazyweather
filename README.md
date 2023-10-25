Entschuldigen Sie bitte die Unannehmlichkeiten. Hier ist das aktualisierte README in der gewünschten Formatierung:


---
# Lazyweather

## Beschreibung

Die Lazyweather-API ist eine Python API, die Wetterdaten von der [open-meteo.com](https://open-meteo.com/en) Webseite bezieht. Lazyweather API gibt die Wetterdaten wie Temperaturen, Windgeschwindigkeiten, Feuchtigkeiten und viele andere Daten zurück.



## Models (`models.py`)

### Location

| Attribute  | Type          | Description                               |
|------------|---------------|-------------------------------------------|
| latitude   | CharField     | Breitengrad des Standorts                 |
| longitude  | CharField     | Längengrad des Standorts                  |
| name       | CharField     | Name des Standorts (kann leer sein)       |

Die `Location`-Model repräsentiert einen geografischen Standort mit Breiten- und Längengrad. Ein Name kann auch für den Standort angegeben werden.

### WeatherData

| Attribute  | Type          | Description                               |
|------------|---------------|-------------------------------------------|
| location   | ForeignKey    | Verknüpfung zum Standort-Model            |
| data       | JSONField     | Speichert die Wetterdaten im JSON-Format  |
| date       | DateField     | Datum der Wetterdaten                     |

Das `WeatherData`-Model speichert die Wetterdaten für einen bestimmten Standort und ein bestimmtes Datum.

---

Now, I will proceed to include the content from `utils.py` and `forms.py`. Shall I continue?

## API-Views

- **location_list**

  | Method | Url              | Erklärung           |
  |--------|------------------|---------------------|
  | GET    | /api/v1/location | Abrufen eines Orts  |
  | POST   |                  | Anlegen eines Orts  |  

- **location_detail**

  | Method | Url                   | Parameter        | Erklärung                |
  |--------|-----------------------|------------------|--------------------------|
  | GET    | /api/v1/location/[pk] | pk : Primary Key | Abrufen eines Orts       |
  | PUT    |                       |                  | Aktualisieren eines Orts |
  | PATCH  |                       |                  | Aktualisieren eines Orts | 
  | DELETE |                       |                  | Löschen eines Orts       |

- **weather_list**

  | Method | Url                   | Erklärung                              |
  |--------|-----------------------|----------------------------------------|
  | GET    | /api/v1/weather-data  | Abrufen von täglichen Witterungsdaten  |
  | POST   |                       | Anlegen von täglichen Witterungsdaten  |

- **weather_detail**

  | Method  | Url                       | Parameter        | Erklärung                                   |
  |---------|---------------------------|------------------|---------------------------------------------|
  | GET     | /api/v1/weather-data/[pk] | pk : Primary Key | Abrufen von täglichen Witterungsdaten       |
  | PUT     |                           |                  | Aktualisieren von täglichen Witterungsdaten |
  | PATCH   |                           |                  | Aktualisieren von täglichen Witterungsdaten |
  | DELETE  |                           |                  | Löschen von täglichen Witterungsdaten       |

- **get_weather_by_location**

  | Method | Url                          | Parameter          | Erklärung                   |
  |--------|------------------------------|--------------------|-----------------------------|
  | GET    | /api/v1/weather/[location]   | location : Adresse | Abrufen von Witterungsdaten |

- **weather_display**

  | Method | Url                          | Erklärung                              |
  |--------|------------------------------|----------------------------------------|
  | GET    | /weather_display             | Abrufen und Anzeigen von Witterungsdaten in einer Vorlage |

- **available_locations**

  | Method | Url                          | Erklärung                              |
  |--------|------------------------------|----------------------------------------|
  | GET    | /available_locations         | Abrufen der verfügbaren Orte           |

- **weather_query (Vue.js Frontend)**

  | Method | Url                          | Parameter          | Erklärung                              |
  |--------|------------------------------|--------------------|----------------------------------------|
  | GET, POST | /weather_query             | location, date, hour | Abfrage und Anzeige von Wetterdaten basierend auf Ort, Datum und Stunde |

  - **Unterfunktionen**
  
    - **get_location**
    - **fetch_weather_data**
    - **fetch_save_new_weather_data**
    - **available_locations**



- **weather_query (Old Version for Django-Frontend Template)**

  | Method | Url                          | Parameter          | Erklärung                              |
  |--------|------------------------------|--------------------|----------------------------------------|
  | GET, POST | /weather_query             | location, date, hour | Abfrage und Anzeige von Wetterdaten in einer Django-Vorlage |


## Utils

- **get_icon_by_weathercode(weathercode)**

  - **Parameter**: weathercode
  - **Erklärung**: Diese Funktion gibt das Wetter-Icon basierend auf dem Wettercode zurück.

- **get_weather_data(location, days=7)**

  - **Parameter**: location, days
  - **Erklärung**: Diese Funktion gibt tägliche Wetterdaten zurück, die von open-meteo.com ab dem heutigen Tag empfangen wurden.

## Forms

- **WeatherQueryForm**

  - **Felder**: location, date, hour
  - **Erklärung**: Dieses Formular wird verwendet, um Wetterdaten basierend auf Ort, Datum und Stunde abzufragen.


## Setup und Installation

1. Navigieren Sie zum Projektverzeichnis:
   ```
   cd lazyweather
   ```

2. Installieren Sie die erforderlichen Pakete:
   ```
   pip install -r requirements.txt
   ```

3. Führen Sie die Django-Migrationen aus:
   ```
   python manage.py migrate
   ```

4. Starten Sie den Django-Entwicklungsserver:
   ```
   python manage.py runserver
   ```

5. Öffnen Sie Ihren Browser und navigieren Sie zu `http://127.0.0.1:8000/`, um auf die Anwendung zuzugreifen.

---



