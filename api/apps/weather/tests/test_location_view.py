from api.apps.weather.models import *
import json
from django.test import TestCase, Client


class LocationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.location_url = 'http://localhost:8000/api/v1/location/'
        cls.payload = {'longitude': 47, 'latitude': 2}
        cls.payload_for_change = {'longitude': 37, 'latitude': 3}
        cls.post_location = cls.client.post(cls.location_url, cls.payload)
        cls.loc = Location.objects.filter(longitude=47, latitude=2).first()
        cls.loc_get_id = cls.loc.id

    def setUp(self):
        pass

    def test_get_locations(self):
        """
        Test : Es werden die Standortinformationen in der Datenbank abgefragt
        Expected :
        status_code = 200
        id, latitude, longitude are not None
        """
        location_get = self.client.get(self.location_url)
        self.assertEqual(location_get.status_code, 200)
        datas = location_get.json()
        for data in datas:
            assert data['id'] is not None
            assert data['latitude'] is not None
            assert data['longitude'] is not None

    def test_post_location(self):
        """
        Test : Es werden die Standortinformationen auf die Datenbank aufgepostet
        Expected :
        status_code = 201
        Daten mit longitude von 47 und latitude von 2 müssen in der Datenbank vorhanden sein
        """
        self.assertEqual(self.post_location.status_code, 201)
        assert self.loc is not None

    def test_get_location_by_pk(self):
        """
        Test : Es werden die gepostete Standortinformationen durch pk aus der Datenbank abgeholt
        Expected : Standortinformationen(longitude, latitude)
        """
        self.post_location
        location = self.client.get(f'http://localhost:8000/api/v1/location/{self.loc_get_id}/')
        assert location is not None
        assert location.json()['longitude'] == '47'
        assert location.json()['latitude'] == '2'

    def test_patch_location(self):
        """
        Test : Es werden die gepostete Standortinformationen gepatcht
        Expected : die gepatchte Standortinformationen
        status_code = 206
        """
        self.post_location
        res = self.client.patch(f'http://localhost:8000/api/v1/location/{self.loc_get_id}/', json.dumps(self.payload_for_change), content_type='application/json')
        self.assertEqual(res.status_code, 206)
        data = res.json()
        loc = Location.objects.filter(longitude=47, latitude=2).first()
        assert loc is None
        assert data['longitude'] == '37'

    def test_delete_location(self):
        """
        Test : Es werden die gepostete Standortinformationen gelöscht
        Expected : Standortinformationen, die in der bestehenden Datenbank vorhanden waren, sollten gelöscht werden.
        status_code = 204
        """
        self.post_location
        res = self.client.delete(f'http://localhost:8000/api/v1/location/{self.loc_get_id}/', json.dumps(self.payload), content_type='application/json')
        self.assertEqual(res.status_code, 204)
        loc = Location.objects.filter(longitude=47, latitude=2).first()
        assert loc is None

    def test_put_location(self):
        """
        Test : Es werden die gepostete Standortinformationen gelöscht
        Expected : Die gepostete Informationen sollten durch die eingestellten Informationen ersetzt werden.
        status_code = 200
        """
        self.post_location
        res = self.client.put(f'http://localhost:8000/api/v1/location/{self.loc_get_id}/', json.dumps(self.payload_for_change), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        loc = Location.objects.filter(longitude=37, latitude=3).first()
        assert loc is not None