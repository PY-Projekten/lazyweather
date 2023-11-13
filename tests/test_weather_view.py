from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from api.apps.weather.models import Location, WeatherData
from api.apps.weather.views import get_location, fetch_weather_data, weather_query
from api.apps.weather.utils import LocationNotFoundError
from unittest.mock import patch, MagicMock
from datetime import datetime, date
#from api.apps.weather.views import weather_q
import json
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
            name=cls.location_name.lower()#,
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
        #cls.date = datetime.strptime('2023-10-18', '%Y-%m-%d').date()  # Ensure this is a date object
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
        #print(WeatherData.objects.all().values())

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
        #self.assertIsNone(weather_data, "The function should return None for an invalid hour.")

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




# Test class for the 'weather_query' API endpoint
class WeatherQueryTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up any necessary objects, like instances of Location or WeatherData
        # This setup will run once for the entire test case

    @classmethod
    def tearDownClass(cls):
        # Clean up any data or reset conditions after the entire test case runs
        super().tearDownClass()

    # # Mock return value for get_location
    # mock_location = Location()
    # mock_location.name = "TestLocation1"
    # mock_location.latitude = 123.45
    # mock_location.longitude = 67.89
    #
    # # Mock return value for get_weather_data
    # mock_weather_data = WeatherData()
    # mock_weather_data.temperature = 20
    # mock_weather_data.humidity = 50
    # mock_weather_data.description = "Sunny"

    @patch('api.apps.weather.utils.get_weather_data')
    @patch('api.apps.weather.views.get_location')
    def test_weather_query_valid_location(self, mock_get_location, mock_get_weather_data):
        # Define mock return values inside the test method
        mock_location = Location(name="Valid Location Name", latitude=123.45, longitude=67.89)
        mock_weather_data = WeatherData(temperature=20, humidity=50, description="Sunny")

        # Set up your mock objects
        mock_get_location.return_value = mock_location  # Replace with appropriate return value
        mock_get_weather_data.return_value = mock_weather_data # Replace with appropriate return value

        # Create a mock POST request object with necessary data
        data = {'location': 'valid_location', 'date': '2023-11-10', 'hour': '12'}
        request = self.factory.post('/api/weather/', data=json.dumps(data), content_type='application/json')

        # Call weather_query with the mock request and a valid location
        response = weather_query(request)

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertIn('expected_weather_data', response.content)

        # Parse the response content and assert the expected data is present
        response_data = json.loads(response.content)
        self.assertIn('data', response_data)
        self.assertEqual(response_data['data']['temperature'], 20)
        self.assertEqual(response_data['data']['humidity'], 50)
        self.assertEqual(response_data['data']['description'], "Sunny")

    @patch('api.apps.weather.views.get_location')
    def test_weather_query_invalid_location(self, mock_get_location):
        # Mock get_location to simulate an invalid location
        mock_get_location.side_effect = LocationNotFoundError('Location not found')

        # Call weather_query with an invalid location
        response = weather_query('invalid_location')

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 404)
        self.assertIn('Location not found', response.content)

    # Add more tests for other scenarios like API failures, database errors, etc.







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
