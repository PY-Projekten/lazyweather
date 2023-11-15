import unittest
from unittest.mock import patch, MagicMock
from api.apps.weather.utils import get_weather_data, LocationNotFoundError
from django.utils import timezone
from api.apps.weather.models import Location, WeatherData
import pytest


class GetWeatherDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup any initial data or mocks here
        cls.location_name = 'Berlin'
        cls.mock_location = Location(longitude='13.41', latitude='52.52', name='berlin')
        cls.mock_weather_data = {
            'date': timezone.now().date().isoformat(),
            'temperature': 20,
            'weather_icon': 'sunny'
        }

    @classmethod
    def tearDownClass(cls):
        # Clean up operations
        pass

    @patch('api.apps.weather.utils.geolocator.geocode')
    @patch('api.apps.weather.utils.requests.Session')
    @pytest.mark.django_db
    def test_successful_data_retrieval(self, mock_session, mock_geocode):
        # Mock the geocode and API call responses
        mock_geocode.return_value = MagicMock(latitude=52.52, longitude=13.41)
        mock_session.return_value.get.return_value.json.return_value = {
            # Mocked API response
        }

        # Call the function
        result = get_weather_data(self.location_name)

        # Assertions
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        # Add more assertions as needed

    @patch('api.apps.weather.utils.geolocator.geocode')
    def test_location_not_found_error(self, mock_geocode):
        # Mock the geocode response for a non-existent location
        mock_geocode.return_value = None

        # Assertions
        with self.assertRaises(LocationNotFoundError):
            get_weather_data('Unknown Location')

    @patch('api.apps.weather.utils.geolocator.geocode')
    @patch('api.apps.weather.utils.requests.Session')
    @pytest.mark.django_db
    def test_database_interaction(self, mock_session, mock_geocode):
        # Mock the geocode and API call responses
        mock_geocode.return_value = MagicMock(latitude=52.52, longitude=13.41)
        mock_session.return_value.get.return_value.json.return_value = {
            # Mocked API response
        }

        # Call the function
        result = get_weather_data(self.location_name)

        # Assertions to check if the data is saved in the database
        # ...

    # Add more test methods as needed

if __name__ == '__main__':
    unittest.main()
