from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils import get_weather_data


@api_view(['GET'])
def get_weather(request, location):
    """
    API view to retrieve the weather data.
    """
    if request.method == 'GET':
        data = get_weather_data(location)
        print(data)
        if data is not None:
            return Response(data, status=200)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_404_BAD_REQUEST)
