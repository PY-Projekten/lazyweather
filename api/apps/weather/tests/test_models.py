from datetime import datetime
from ..models import Location
from django.test import TestCase


class LocationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.location = Location.objects.create(
            latitude="30.33",
            longitude="13.33"

        )

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_location_exists(self):
        loc = Location.objects.filter(longitude=self.location.longitude, latitude=self.location.latitude).first()

        assert loc is not None


    def test_location_not_exists(self):
        loc = Location.objects.filter(longitude=12, latitude=8).first()

        assert loc is None

