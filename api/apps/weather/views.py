from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import LocationSerializer, WeatherDataSerializer
from django.shortcuts import render
from .forms import WeatherQueryForm
from .utils import get_weather_data
import logging
from datetime import datetime
logger = logging.getLogger(__name__)
from django.http import JsonResponse





# Create your views here.


@api_view(['GET', 'POST'])
def location_list(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def location_detail(request, pk):
    """
    API view zum Abrufen, Aktualisieren oder Löschen eines Orts.
    """
    try:
        location = Location.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def weather_list(request):
    """
    API view zum Abrufen oder zum Anlegen von täglichen Witterungsdaten.
    """
    if request.method == 'GET':
        res = []
        weathers = WeatherData.objects.filter(location__name='hamburg')
        # for w in weathers:
        #     if w.location.name == 'hamburg':
        #         res.append(w)

        serializer = WeatherDataSerializer(weathers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = WeatherDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_weather_by_location(request, location):
    """"""
    if request.method == "GET":

        location = Location.objects.filter(name=location).first()

        wd = WeatherData.objects.filter(location=location)
        serializer = WeatherDataSerializer(wd, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def weather_detail(request, pk):
    """
    API view zum Abrufen, Aktualisieren oder Löschen von täglichen Witterungsdaten.
    """
    try:
        weather = WeatherData.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WeatherDataSerializer(weather)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = WeatherDataSerializer(weather, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = WeatherDataSerializer(weather, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        weather.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def weather_display(request):
    """
    API view zum Abrufen oder zum Anlegen von täglichen Witterungsdaten.
    """
    # Check for the template quer
    if request.method == 'GET':
        # Fetch the weather data for Hamburg (as it's currently hardcoded to "hamburg")
        weather_data = get_weather_data('Hamburg')  # This fetches the structured weather data

        # Use the fetched weather data as context for the template
        context = {
            'location_name': 'Hamburg',  # This can be made dynamic later
            'weather_data': weather_data,
        }

        # Render the template with the context data
        return render(request, 'myfirst.html', context)

    # if request.method == 'GET':
    #     res = []
    #     weathers = WeatherData.objects.filter(location__name='hamburg')
    #     # for w in weathers:
    #     #     if w.location.name == 'hamburg':
    #     #         res.append(w)
    #
    #     serializer = WeatherDataSerializer(weathers, many=True)
    #     return Response(serializer.data)
    # elif request.method == 'POST':
    #     serializer = WeatherDataSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUES


def available_locations(request):
    locations = Location.objects.all().values_list('name', flat=True)
    return JsonResponse({'locations': list(locations)}, safe=False)





#Successufly retrieves and posts existing data from the database
# @api_view(['GET', 'POST'])
# def weather_query(request):
#     response_data = {
#         'status': 'error',
#         'message': 'An unexpected error occurred.'
#     }
#
#     if request.method == "POST":
#         location_name = request.data.get('location')
#         date = request.data.get('date')
#         hour = request.data.get('hour')  # Hour can be None
#
#         location = Location.objects.filter(name=location_name.lower()).first()
#
#         if location:
#             query_results = WeatherData.objects.filter(location=location, date=date)
#
#             if query_results.exists():
#                 entry = query_results.last().data
#
#                 # Check if entry is a list and get the first element if it is
#                 if isinstance(entry, list):
#                     entry = entry[0]
#
#                 date_data = entry.get(date, {}).get('weather_times', {})
#
#                 response_data['data'] = []
#
#                 for h, hour_data in date_data.items():
#                     if hour and h.zfill(2) != hour.zfill(2):  # Ensure hour format matches
#                         continue
#                     response_data['data'].append({
#                         'date': date,
#                         'hour': h.zfill(2),
#                         'temperature': hour_data.get('temp')
#                     })
#
#                 if response_data['data']:
#                     response_data['status'] = 'success'
#                     response_data['message'] = 'Data processed successfully.'
#                 else:
#                     response_data['message'] = 'No weather data available for the specified hour.'
#             else:
#                 response_data['message'] = 'No weather data available for the specified date and location.'
#         else:
#             response_data['message'] = 'Location does not exist.'
#
#     return JsonResponse(response_data)




#Modularization of Weather Query Version 2
# @api_view(['GET', 'POST'])
# def weather_query(request):
#     if request.method != "POST":
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
#
#     location_name = request.data.get('location')
#     date = request.data.get('date')
#     hour = request.data.get('hour')  # Hour can be None
#
#     # Check if location_name is None or empty
#     if not location_name:
#         return JsonResponse({'status': 'error', 'message': 'Location is required.'})
#
#     location = get_location(location_name)
#     if not location:
#         return JsonResponse({'status': 'error', 'message': 'Location does not exist.'})
#
#     weather_data = fetch_weather_data(location, date, hour)
#     if not weather_data:
#         return JsonResponse({'status': 'error', 'message': 'No weather data available for the specified parameters.'})
#
#     return JsonResponse({'status': 'success', 'message': 'Data processed successfully.', 'data': weather_data})
#
#
# def get_location(location_name):
#     return Location.objects.filter(name=location_name.lower()).first()
#
#
# def fetch_weather_data(location, date, hour):
#     query_results = WeatherData.objects.filter(location=location, date=date)
#     if not query_results.exists():
#         return None
#
#     entry = query_results.last().data
#
#     # Handling the case where entry is a list
#     if isinstance(entry, list):
#         entry = entry[0] if entry else {}
#
#     date_data = entry.get(date, {}).get('weather_times', {})
#
#     # Filtering and processing logic here
#     weather_data = []
#     for h, hour_data in date_data.items():
#         if hour and h.zfill(2) != hour.zfill(2):  # Ensure hour format matches
#             continue
#         weather_data.append({
#             'date': date,
#             'hour': h.zfill(2),
#             'temperature': hour_data.get('temp')
#         })
#
#     return weather_data




# Implement and test the functionality to handle new location queries,
# fetch the corresponding weather data from an external API,
# update the database, and display the results on the frontend.
@api_view(['GET', 'POST'])
def weather_query(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    location_name = request.data.get('location')
    date = request.data.get('date')
    hour = request.data.get('hour')  # Hour can be None

    temp = get_weather_data(location_name)

    print(temp)
    # Check if location_name is None or empty
    #if not location_name:
    #    return JsonResponse({'status': 'error', 'message': 'Location is required.'})

    location = get_location(location_name)
    if not location:
        return JsonResponse({'status': 'error', 'message': 'Location does not exist.'})

    # Check if the weather data for the location is in the database
    existing_data = WeatherData.objects.filter(location=location)

    if not existing_data.exists():
        weather_data = fetch_save_new_weather_data(location)
    else:
        weather_data = get_weather_data(location)

    weather_data = fetch_weather_data(location, date, hour)
    if not weather_data:
        return JsonResponse({'status': 'error', 'message': 'No weather data available for the specified parameters.'})

    return JsonResponse({'status': 'success', 'message': 'Data processed successfully.', 'data': weather_data})


# Enhancing weather_query to accept new locations
# @api_view(['GET', 'POST'])
# def weather_query(request):
#     if request.method != "POST":
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
#
#     location_name = request.data.get('location')
#     date = request.data.get('date')
#     hour = request.data.get('hour')  # Hour can be None
#
#     # Check if location_name is None or empty
#     if not location_name:
#         return JsonResponse({'status': 'error', 'message': 'Location is required.'})
#
#     location = get_location(location_name)
#     # If location does not exist in the database, fetch and save new weather data
#     if not location:
#         success = fetch_save_new_weather_data(location_name)
#         if not success:
#             return JsonResponse({'status': 'error', 'message': 'Failed to fetch new location data.'})
#         location = get_location(location_name) # Re-fetch the location after saving new data
#
#     weather_data = fetch_weather_data(location, date, hour)
#     if not weather_data:
#         return JsonResponse({'status': 'error', 'message': 'No weather data available for the specified parameters.'})
#
#     return JsonResponse({'status': 'success', 'message': 'Data processed successfully.', 'data': weather_data})


def get_location(location_name):
    return Location.objects.filter(name=location_name.lower()).first()


def fetch_weather_data(location, date, hour):
    query_results = WeatherData.objects.filter(location=location, date=date)
    if not query_results.exists():
        return None

    entry = query_results.last().data

    # Handling the case where entry is a list
    if isinstance(entry, list):
        entry = entry[0] if entry else {}

    date_data = entry.get(date, {}).get('weather_times', {})

    # Filtering and processing logic here
    weather_data = []
    for h, hour_data in date_data.items():
        if hour and h.zfill(2) != hour.zfill(2):  # Ensure hour format matches
            continue
        weather_data.append({
            'date': date,
            'hour': h.zfill(2),
            'temperature': hour_data.get('temp')
        })

    return weather_data


def fetch_save_new_weather_data(location):
    # Fetch data from the external API
    fetched_data = fetch_data_from_api(location)  # Assuming you have a function to fetch data from the API

    # Process and save the fetched data in the database
    processed_data = process_fetched_data(fetched_data)  # Assuming you have a function to process the data
    WeatherData.objects.create(location=location, data=processed_data)

    return processed_data
