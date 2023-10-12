from rest_framework import serializers
from api.apps.weather.models import Location, WeatherData


class LocationSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Location
        fields = '__all__'


class WeatherDataSerializer(serializers.ModelSerializer):
    """
    Weather Serializer
    """
    class Meta:
        model = WeatherData
        fields = "__all__"
