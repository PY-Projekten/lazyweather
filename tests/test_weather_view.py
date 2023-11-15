from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from requests import RequestException

from api.apps.weather.models import Location, WeatherData
from api.apps.weather.views import get_location, fetch_weather_data, weather_query
from api.apps.weather.serializers import LocationSerializer
from api.apps.weather.utils import LocationNotFoundError
from unittest.mock import patch, MagicMock
from datetime import datetime, date
# from api.apps.weather.views import weather_q
import json
import logging


class AvailableLocationsTest(TestCase):
    """Test cases for the available_locations endpoint."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.url = reverse('available_locations')

    @patch('api.apps.weather.views.Location.objects.all')
    def test_available_locations_returns_correct_data(self, mock_all):
        # Create a MockSet
        mock_qs = MagicMock()
        # Mock the 'values' method to return a list of dictionaries with the location data
        mock_qs.values_list.return_value = ['Location1', 'Location2']

        # Set this mock QuerySet to be the return value of Location.objects.all()
        mock_all.return_value = mock_qs

        # Making a GET request to the available_locations endpoint
        response = self.client.get(self.url)

        # Expected data based on the mock locations
        expected_data = {'locations': ['Location1', 'Location2']}

        # Assertions to check the status code and the returned data
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_data)

    # Test class for the 'get_location' utility function


class GetLocationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a Location object for the test class
        cls.location_name = 'TestLocation1'
        cls.location = Location.objects.create(
            name=cls.location_name.lower()  # ,
            # latitude='123',
            # longitude='456'
        )

    @classmethod
    def tearDownClass(cls):
        # Clean up after all tests have run
        cls.location.delete()
        super().tearDownClass()

    def test_get_location_with_existing_name(self):
        #     # Test to ensure get_location returns the correct location for an existing name
        # Call the get_location function with the name of the location
        location = get_location(self.location_name)
        # Check that the location returned is not None
        self.assertIsNotNone(location, 'The location should not be None')
        # Check that the location's name matches the name used to create it
        self.assertEqual(location.name, self.location_name.lower())

    def test_get_location_with_non_existing_name(self):
        # Test that get_location returns None for a non-existing name
        location = get_location('NonExistingLocation')
        self.assertIsNone(location)

    def test_get_location_with_different_cases(self):
        # Test the function with various cases
        self.assertIsNotNone(get_location('TESTLOCATION1'))
        self.assertIsNotNone(get_location('testlocation1'))
        self.assertIsNotNone(get_location('TestLocation1'))
        #
        # You could also assert that the returned object has the correct attributes
        location_upper = get_location('TESTLOCATION1')
        location_lower = get_location('testlocation1')
        location_capitalized = get_location('TestLocation1')

        # Ensure that the correct object is returned for each case
        self.assertEqual(location_upper.name, 'testlocation1')
        self.assertEqual(location_lower.name, 'testlocation1')
        self.assertEqual(location_capitalized.name, 'testlocation1')

        # You could also assert that the returned object has the correct attributes
        location = get_location('TESTLOCATION1')
        self.assertEqual(location.name, 'testlocation1')
        # self.assertEqual(location.latitude, '123')
        # self.assertEqual(location.longitude, '456')

    def test_get_location_with_empty_string(self):
        # Test that get_location returns None when an empty string is passed
        location = get_location('')
        self.assertIsNone(location)


# Test class for the 'fetch_weather_data' utility function
class FetchWeatherDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data for location and weather data
        cls.location = Location.objects.create(name='TestLocation', latitude='123', longitude='456')
        # cls.date = datetime.strptime('2023-10-18', '%Y-%m-%d').date()  # Ensure this is a date object
        cls.date = '2023-10-18'
        cls.hour = '12'
        cls.weather_data_entry = {
            str(cls.date): {
                'weather_times': {
                    cls.hour.zfill(2): {'temp': 20}
                }
            }
        }
        cls.weather_data = WeatherData.objects.create(
            location=cls.location,
            date=cls.date,
            data=cls.weather_data_entry  # Assuming 'data' is a JSONField or similar
        )
        # print(WeatherData.objects.all().values())

    def test_fetch_weather_data_with_valid_input(self):
        # Test the function with valid location, date, and hour
        weather_data = fetch_weather_data(
            location=self.location,
            date=self.date,
            hour=self.hour
        )
        print(weather_data)
        self.assertIsNotNone(weather_data)
        self.assertEqual(len(weather_data), 1)
        self.assertEqual(weather_data[0]['temperature'], 20)

    def test_fetch_weather_data_with_invalid_location(self):
        # Test the function with an invalid location
        invalid_location = Location(name='InvalidLocation', latitude='999', longitude='999')
        weather_data = fetch_weather_data(
            location=invalid_location,
            date=self.date,
            hour=self.hour
        )
        self.assertIsNone(weather_data, "The function should return None for an invalid location.")

    def test_fetch_weather_data_with_invalid_date(self):
        # Test the function with an invalid date
        invalid_date = datetime(1999, 1, 1).date()
        weather_data = fetch_weather_data(
            location=self.location,
            date=invalid_date,
            hour=self.hour
        )
        self.assertIsNone(weather_data, "The function should return None for an invalid date.")

    def test_fetch_weather_data_with_invalid_hour(self):
        # Test the function with an invalid hour
        invalid_hour = '25'  # Assuming hour should be within "00"-"23"
        weather_data = fetch_weather_data(
            location=self.location,
            date=self.date,
            hour=invalid_hour
        )
        self.assertEqual(weather_data, [], "The function should return an empty list for an invalid hour.")
        # self.assertIsNone(weather_data, "The function should return None for an invalid hour.")

    def test_fetch_weather_data_filters_by_hour(self):
        # Test the function's ability to filter by hour
        # Assuming there is more than one WeatherData object for the same date but different hours
        WeatherData.objects.create(
            location=self.location,
            date=self.date,
            data={
                str(self.date): {
                    'weather_times': {
                        '06': {'temp': 15}
                    }
                }
            }
        )
        weather_data = fetch_weather_data(
            location=self.location,
            date=self.date,
            hour='06'
        )
        self.assertIsNotNone(weather_data)
        self.assertEqual(len(weather_data), 1)
        self.assertEqual(weather_data[0]['hour'], '06')
        self.assertEqual(weather_data[0]['temperature'], 15)


# *** Serializer Version
class WeatherQueryTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up shared objects here
        cls.factory = RequestFactory()
        cls.location = Location.objects.create(
            latitude='40.7128', longitude='-74.0060', name='New York'
        )
        WeatherData.objects.create(
            location=cls.location,
            data={
                timezone.now().date().isoformat(): {
                    'weather_times': {
                        '15': {'temp': 20}
                    }
                }
            },
            date=timezone.now().date()
        )
        # Set up logging
        logging.basicConfig(level=logging.DEBUG)
        cls.logger = logging.getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        # Delete WeatherData
        WeatherData.objects.all().delete()

        # Delete location
        cls.location.delete()

        super().tearDownClass()

    @patch('api.apps.weather.views.fetch_weather_data')
    @patch('api.apps.weather.views.get_location')
    def test_weather_query_valid_location(self, mock_get_location, mock_fetch_weather_data):
        # Define mock return values inside the test method
        mock_get_location.return_value = self.location

        mock_fetch_weather_data.return_value = [{
            'date': timezone.now().date().isoformat(),
            'hour': '15',
            'temperature': 20
        }]

        # Create a mock POST request object with necessary data
        data = {
            'location': 'New York',
            'date': timezone.now().date().isoformat(),
            'hour': '15'
        }
        request = self.factory.post('weather_query', data, content_type='application/json')

        # Call weather_query with the mock request
        response = weather_query(request)

        # Inspect the response content
        response_content = response.content.decode('utf-8')
        self.logger.debug("Response content: %s", response_content)

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertIn('Data processed successfully.', str(response.content))
        # # Additional checks for the content of the response
        # print('R: ', json.dumps(response))
        response_content = json.loads(response_content)
        self.assertIn('location', response_content['data'])
        self.assertIn('weather', response_content['data'])
        #
        # New: Verify the structure and content of the serialized location
        serialized_location = LocationSerializer(response_content['data']['location']).data
        print(serialized_location)
        self.assertEqual(serialized_location['name'], 'New York')
        self.assertEqual(serialized_location['latitude'], '40.7128')
        self.assertEqual(serialized_location['longitude'], '-74.0060')

    @patch('api.apps.weather.views.fetch_weather_data')
    @patch('api.apps.weather.views.get_location')
    def test_weather_query_invalid_location(self, mock_get_location, mock_fetch_weather_data):
        # Mock get_location to return None or raise an exception for an invalid location
        mock_get_location.side_effect = LocationNotFoundError("Invalid location")

        # Mock fetch_weather_data as needed, though it might not be called if get_location fails
        # ...
        mock_fetch_weather_data.return_value = [{
            'date': timezone.now().date().isoformat(),
            'hour': '15',
            'temperature': 20
        }]

        # Create a mock POST request object with invalid location data
        data = {
            'location': 'InvalidLocation',
            'data': timezone.now().date().isoformat(),
            'hour': 15
        }
        request = self.factory.post('weather_query', data, content_type='application/json')

        # Call weather_query with the mock request
        response = weather_query(request)

        # Inspect the response content
        response_content = response.content.decode('utf-8')
        self.logger.debug("response content: %s", response_content)

        # Assert that the response indicates an error due to invalid location
        self.assertEqual(response.status_code, 404)
        self.assertIn("Location 'InvalidLocation' not found", response_content)

    @patch('api.apps.weather.views.fetch_weather_data')
    @patch('api.apps.weather.views.get_location')
    def test_weather_query_no_data_available(self, mock_get_location, mock_fetch_weather_data):
        # Define mock return values inside the test method
        mock_get_location.return_value = self.location
        # Create a mock POST request object with a valid location but no data for the requested date/hour

        mock_fetch_weather_data.return_value = []

        data = {
            'location': 'New York',
            'date': '2023-11-15',  # Use a date for which no data is available
            'hour': 15
        }
        request = self.factory.post('weather_query', data, content_type='application/json')

        # Call weather_query with the mock request
        response = weather_query(request)

        # Inspect the response content
        response_content = response.content.decode('utf-8')
        self.logger.debug("Response content: %s", response_content)

        # Assert that the response indicates no data available
        self.assertEqual(response.status_code, 404)  # Or another appropriate status code
        self.assertIn('No weather data available', response.content.decode('utf-8'))

    @patch('api.apps.weather.views.fetch_weather_data')
    @patch('api.apps.weather.views.get_location')
    def test_weather_query_missing_location(self, mock_get_location, mock_fetch_weather_data):
        # Create a mock POST request object without a location field
        data = {
            'date': timezone.now().date().isoformat(),
            'hour': 15
        }
        request = self.factory.post('weather_query', data, content_type='application/json')

        # Call weather_query with the mock request
        response = weather_query(request)

        # Inspect the response content
        response_content = response.content.decode('utf-8')
        self.logger.debug("Response content: %s", response_content)

        # Assert that the response indicates an error due to missing location
        self.assertEqual(response.status_code, 400)
        self.assertIn('Location is required', response_content)


    def test_weather_query_invalid_request_method(self):
        # Create a mock GET request object
        request = self.factory.get('weather_query')

        # Call weather_query with the mock request
        response = weather_query(request)

        # Render the response before accessing its content
        response.render()

        # Inspect the response content
        response_content = response.content.decode('utf-8')
        self.logger.debug("Response content: %s", response_content)

        # try:
        #     response_data = json.loads(response_content)
        #     self.logger.debug("Parsed response data: %s", response_data)
        # except json.JSONDecodeError:
        #     self.fail("Response content is not valid JSON")

        # Assert that the response indicates an invalid request method
        self.assertEqual(response.status_code, 405)
        self.assertIn('"Method \\"GET\\" not allowed."', response_content)

    @patch('api.apps.weather.views.fetch_weather_data')
    def test_weather_query_external_api_failure(self, mock_fetch_weather_data):
        mock_fetch_weather_data.side_effect = RequestException("External API error")

        # Create a mock POST request object
        data = {'location': 'New York', 'date': '2023-11-15', 'hour': 15}
        request = self.factory.post('weather_query', data, content_type='application/json')

        # Call weather_query with the mock request
        response = weather_query(request)

        # Inspect the response content
        response_content = response.content.decode('utf-8')
        self.logger.debug("Response content: %s", response_content)

        # Assert that the response indicates an external API failure
        self.assertEqual(response.status_code, 503)
        self.assertIn('Failed to retrieve weather data due to an external error', response_content)


    # ** Test Version
    @patch('api.apps.weather.views.fetch_weather_data')
    def test_weather_query_unexpected_error(self, mock_fetch_weather_data):
        mock_fetch_weather_data.side_effect = Exception("Unexpected error")

        # Create a mock POST request object
        data = {'location': 'New York',
                'date': '2023-11-15',
                'hour': 15
                }

        request = self.factory.post('weather_query', data, content_type='application/json')

        # Call weather_query with the mock request
        response = weather_query(request)

        # Inspect the response content
        response_content = response.content.decode('utf-8')
        self.logger.debug("Response content: %s", response_content)

        # Assert that the response indicates an unexpected error
        self.assertEqual(response.status_code, 500)
        self.assertIn('An unexpected error occurred', response_content)

    # @classmethod
    # def setUpClass(cls):
    #     cls.client = Client()
    # #
    # # def test_get_weather_q(self):
    # #     response = self.client.get('http://localhost:8000/api/v1/available_locations/')
    # #     print(response, "resonse")
    # #     self.assertEqual(len(response.data), 21)
    # #     self.assertEqual(response.status_code, 200)
    # #
    # @classmethod
    # def tearDownClass(cls):
    #     pass
    #
    # def test_get_available_locations(self):
    #
    #     pass
    #
    # def test_get_location(self):
    #     pass
    #
    # def test_fetch_weather_data(self):
    #     pass
    #
    # def test_fetch_save_new_weather_data(self):
    #     pass
