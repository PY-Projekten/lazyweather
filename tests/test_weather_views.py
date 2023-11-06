from django.test import TestCase
from django.urls import reverse
import json

class WeatherViewTests(TestCase):
    def test_weather_query_view(self):
        url = reverse('weather_query')
        data = json.dumps({
            'location': 'hamburg',
            'date': '2023-10-18',
            'hour': '02'
        })
        response = self.client.post(url, data, content_type= 'application/json')
        self.assertEqual(response.status_code, 200)
