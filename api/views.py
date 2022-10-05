from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.apps.weather.utils import get_weather_data
from rest_framework import serializers

@api_view(['GET'])
def get_weather(request, location):
    """
    API view to retrieve the weather data.
    """
    if request.method == 'GET':
        data = get_weather_data(location)

        if data is not None:
            return Response(data, status=200)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_404_BAD_REQUEST)
