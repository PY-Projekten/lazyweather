from django.test import TestCase, Client
from django.urls import reverse
from api.apps.weather.views import Location
from unittest.mock import patch, MagicMock

from api.apps.weather.views import weather_q
class AvailableLocationsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.url = reverse('available_locations')

        # Location.objects.create(latitude='123', longitude='456', name='Location1')
        # Location.objects.create(latitude='789', longitude='101', name='Location2')

    # @classmethod
    # def tearDownClass(cls):
    #     # Deleting mock location data
    #     super().tearDownClass()
    #     Location.objects.all().delete()

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
