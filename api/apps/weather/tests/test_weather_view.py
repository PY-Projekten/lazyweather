from api.apps.weather.models import *
import json
from django.test import TestCase, Client


class WeatherViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.weather_url = 'http://localhost:8000/api/v1/weather-data/'
        cls.loc = Location.objects.create(longitude='32', latitude='11')
        cls.test = [
            {
                "2022-10-07": {
                    "temp_max": 16.4,
                    "temp_min": 8.3,
                    "precipitation_sum": 0.0,
                    "snowfall_sum": 0.0,
                    "temp_current": 9.2,
                    "weather_times": {
                        "00": {
                            "temp": 10.2,
                            "cloudcover": 0.0,
                            "precipitation": 0.0,
                            "snowfall": 0.0,
                            "weathercode": 0.0,
                            "weather_icon": {
                                "icon": "mdi-weather-sunny",
                                "color": "yellow",
                                "description": "Klar"
                            }
                        },
                        "01": {
                            "temp": 9.7,
                            "cloudcover": 0.0,
                            "precipitation": 0.0,
                            "snowfall": 0.0,
                            "weathercode": 0.0,
                            "weather_icon": {
                                "icon": "mdi-weather-sunny",
                                "color": "yellow",
                                "description": "Klar"
                            }
                        },
                        "02": {
                            "temp": 9.2,
                            "cloudcover": 0.0,
                            "precipitation": 0.0,
                            "snowfall": 0.0,
                            "weathercode": 0.0,
                            "weather_icon": {
                                "icon": "mdi-weather-sunny",
                                "color": "yellow",
                                "description": "Klar"
                            }
                        },
                        }
                        }
                        }]
        cls.loc_id = cls.loc.id
        cls.payload = {'location': cls.loc_id, 'data': json.dumps(cls.test), 'date': '2022-10-14'}
        cls.payload_for_change = {'location': cls.loc_id, 'data': json.dumps([]), 'date': '2022-10-14'}

    def setUp(self):
        pass

    def test_get_weather_data(self):
        """
        Test : Es werden die Wetterinformationen in der Datenbank abgefragt
        Expected : datas are not None
        status_code = 200
        """
        weather_get = self.client.get(self.weather_url)
        self.assertEqual(weather_get.status_code, 200)
        datas = weather_get.json()
        assert datas is not None

    def test_post_weather_data(self):
        """
        Test : Es werden die Wetterinformationen auf die Datenbank aufgepostet
        Expected : Die gepostete Wetterinformationen müssen in der Datenbank vorhanden sein
        status_code = 201
        """
        res = self.client.post(self.weather_url, self.payload)
        self.assertEqual(res.status_code, 201)
        assert res.json()['date'] == '2022-10-14'
        assert res.json()['data'] == self.test
        assert type(res.json()['data'][0]) == dict
        assert res.json()['data'][0]['2022-10-07'] == self.test[0]['2022-10-07']

    def test_get_weather_data_detail(self):
        """
        Test : Es werden die detailierte Wetterinformationen durch pk aus der Datenbank abgeholt
        Expected : Detailierte Wetterdaten
        status_code = 200
        """
        res = self.client.post(self.weather_url, self.payload)
        self.assertEqual(res.status_code, 201)
        weather_id = (res.json())['id']
        assert weather_id is not None
        assert weather_id == 1
        res = self.client.get(f'{self.weather_url}{weather_id}/')
        self.assertEqual(res.status_code, 200)
        temp = res.json()
        assert temp['date'] == '2022-10-14'

    def test_put_weather_data_detail(self):
        """
        Test : Es werden die gepostete Wetterinformationen geändert
        Expected : Die gepostete informationen sollten durch die eingestellten Informationen ersetzt werden.
        status_code = 200
        """
        res = self.client.post(self.weather_url, self.payload)
        self.assertEqual(res.status_code, 201)
        weather_id = (res.json())['id']
        assert weather_id is not None
        assert weather_id == 1
        put = self.client.put(f'{self.weather_url}{weather_id}/', json.dumps(self.payload_for_change), content_type='application/json')
        self.assertEqual(put.status_code, 200)
        temp = put.json()
        assert temp['data'] == '[]'

    def test_patch_weather_data_detail(self):
        """
        Test : Es werden die gepostete Wetterinformationen gepatcht
        Expected : die gepatchte Wetterinformationen
        status_code = 200
        """
        res = self.client.post(self.weather_url, self.payload)
        self.assertEqual(res.status_code, 201)
        weather_id = (res.json())['id']
        assert weather_id is not None
        assert weather_id == 1
        patch = self.client.patch(f'{self.weather_url}{weather_id}/', json.dumps(self.payload_for_change), content_type='application/json')
        self.assertEqual(patch.status_code, 200)
        temp = patch.json()
        assert temp['data'] == '[]'

    def test_delete_weather_data_detail(self):
        """
        Test : Es werden die gepostete Wetterinformationen gelöscht
        Expected : Wetterinformationen, die in der bestehenden Datenbank vorhanden waren, sollten gelöscht werden.
        status_code = 204
        """
        res = self.client.post(self.weather_url, self.payload)
        self.assertEqual(res.status_code, 201)
        weather_id = (res.json())['id']
        assert weather_id is not None
        assert weather_id == 1
        delete = self.client.delete(f'{self.weather_url}{weather_id}/', json.dumps(self.payload), content_type='application/json')
        self.assertEqual(delete.status_code, 204)
        delete_data = WeatherData.objects.filter(date='2022-10-14')
        self.assertQuerysetEqual(delete_data, [])
