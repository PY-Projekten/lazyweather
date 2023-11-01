from django.test import TestCase
from django.urls import reverse

class WeatherViewTests(TestCase):
    def test_weather_query_view(self):
        url = reverse('weather_query')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
