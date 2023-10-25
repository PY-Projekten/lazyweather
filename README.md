
# Lazyweather

## Beschreibung

Die Lazyweather-API ist eine Python API, die Wetterdaten von der [open-meteo.com](https://open-meteo.com/en) Webseite bezieht. Lazyweather API gibt die Wetterdaten wie Temperaturen, Windgeschwindigkeiten, Feuchtigkeiten und viele andere Daten zurück.

## API-Views

- **get_weather**

  | Method | Url                          | Parameter          | Erklärung                   |
  |--------|------------------------------|--------------------|-----------------------------|
  | GET    | /api/v1/weather/[location]   | location : Adresse | Abrufen von Witterungsdaten |

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

