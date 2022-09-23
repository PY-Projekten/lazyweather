from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils import latitude_longitude


@api_view(['GET'])
def get_weather(request, location):

    if request.method == 'GET':
        data = latitude_longitude(location)
        print(data)
        if data:
            return Response(data, status=200)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_404_BAD_REQUEST)
