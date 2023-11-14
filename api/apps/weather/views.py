from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import LocationSerializer, WeatherDataSerializer
from django.shortcuts import render
from .forms import WeatherQueryForm
from .utils import get_weather_data, LocationNotFoundError
import logging
from datetime import datetime
logger = logging.getLogger(__name__)
from django.http import JsonResponse
#from .exceptions import ExternalAPIError
from requests.exceptions import RequestException






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



# *** Version: old weather_query method for django-frontend Template (weather_query_template.html), that ***
# +++ this also corresponds with forms.py +++

# def weather_query(request):
#     form = WeatherQueryForm(request.POST or None, initial={'date': datetime.now().date()})
#     context = {'form': form}
#
#     # Query all location names and pass them to the context
#     locations = Location.objects.all().values_list('name', flat=True)
#     context['locations'] = list(locations)
#
#     if request.method == "POST" and form.is_valid():
#         location_name = form.cleaned_data['location']
#         date = form.cleaned_data['date']
#         date_str = date.strftime('%Y-%m-%d')  # Correctly formatting the date as a string
#         hour = form.cleaned_data['hour']
#         # This line checks if a POST variable named confirmed exists and if its value is "true".
#         # This variable is set by the JavaScript code when the user confirms the addition of a new location.
#         confirmed = request.POST.get('confirmed') == "true"
#         print(f"Confirmed: {confirmed}")
#
#         location = None
#         try:
#             location = Location.objects.get(name=location_name.lower())
#         except ObjectDoesNotExist:
#             pass
#         print(f"Location: {location}")
#
#         # This condition checks if the location does not exist in the database
#         # and if the user has not confirmed the addition of the new location.
#         if not location and not confirmed:
#             return render(request, 'weather_query_template.html', context)
#
#         # If the location is newly created or weather data is not available, fetch it
#         if not location:
#             get_weather_data(location_name)
#
#         query_results = WeatherData.objects.filter(location=location, date=date_str)
#
#         if query_results.exists():
#             entry = query_results.last().data
#
#             # Check if entry is a list and get the first element if it is
#             if isinstance(entry, list):
#                 entry = entry[0]
#
#             day_data = entry.get(str(date), {})
#             weather_times = day_data.get('weather_times', {})
#
#             context['data'] = []
#
#             if hour:  # An hour is selected
#                 hour_data = weather_times.get(hour, {})
#                 context['data'].append({'date': date_str, 'hour': hour, 'temperature': hour_data.get('temp')})
#             else:  # No hour is selected, display all hours
#                 for h, hour_data in weather_times.items():
#                     context['data'].append({'date': date_str, 'hour': h, 'temperature': hour_data.get('temp')})
#
#     return render(request, 'weather_query_template.html', context)




def available_locations(request):
    locations = Location.objects.all().values_list('name', flat=True)
    print(len(locations))
    return JsonResponse({'locations': list(locations)}, safe=False)



# @api_view(['POST'])
# def weather_query(request):
#     # Ensure only POST requests are handled
#     if request.method != "POST":
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     # Extract and validate request data
#     location_name = request.data.get('location')
#     date = request.data.get('date')
#     hour = request.data.get('hour')  # Hour can be None
#
#     # Check if location_name is None or empty
#     if not location_name:
#        return JsonResponse({'status': 'error', 'message': 'Location is required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#     try:
#         # Now we can safely call get_weather_data
#         get_weather_data(location_name)
#         location = get_location(location_name)
#         if not location:
#             return JsonResponse({'status': 'error', 'message': 'Location does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#
#         # Now we can safely call get_weather_data
#         weather_data = fetch_weather_data(location, date, hour)
#         if not weather_data:
#             return JsonResponse({'status': 'error', 'message': 'No weather data available for the specified parameters.'}, status=status.HTTP_404_NOT_FOUND)
#
#     except LocationNotFoundError as e:
#         # Handle location not found error
#         logger.error(f"LocationNotFoundError caught: {e}")
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
#
#     #except ExternalAPIError as e:
#     except RequestException as e:
#         # Handle specific known error (e.g., ExternalAPIError is a custom exception)
#         logger.error(f"Request error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': 'Failed to retrieve weather data due to an external error.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     except Exception as e:
#         # Handle unexpected errors
#         logger.error(f"Unexpected error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': 'An unexpected error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     return JsonResponse({'status': 'success', 'message': 'Data processed successfully.', 'data': weather_data}, status=status.HTTP_200_OK)


#** Serializer Version weather_query **
# @api_view(['POST'])
# def weather_query(request):
#     # Ensure only POST requests are handled
#     if request.method != "POST":
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     # Extract and validate request data
#     location_name = request.data.get('location')
#     date = request.data.get('date')
#     hour = request.data.get('hour')  # Hour can be None
#
#     # Check if location_name is None or empty
#     if not location_name:
#        return JsonResponse({'status': 'error', 'message': 'Location is required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#     try:
#         # Now we can safely call get_weather_data
#         get_weather_data(location_name)
#         location = get_location(location_name)
#         if not location:
#             return JsonResponse({'status': 'error', 'message': 'Location does not exist.'}, status=status.HTTP_404_NOT_FOUND)
#
#         # Serialize the location object
#         location_serialized = LocationSerializer(location).data
#
#         # Now we can safely call get_weather_data
#         weather_data = fetch_weather_data(location, date, hour)
#         if not weather_data:
#             return JsonResponse({'status': 'error', 'message': 'No weather data available for the specified parameters.'}, status=status.HTTP_404_NOT_FOUND)
#
#     except LocationNotFoundError as e:
#         # Handle location not found error
#         logger.error(f"LocationNotFoundError caught: {e}")
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
#
#     #except ExternalAPIError as e:
#     except RequestException as e:
#         # Handle specific known error (e.g., ExternalAPIError is a custom exception)
#         logger.error(f"Request error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': 'Failed to retrieve weather data due to an external error.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     except Exception as e:
#         # Handle unexpected errors
#         logger.error(f"Unexpected error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': 'An unexpected error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     # Combine location data with weather data
#     response_data = {
#         'location': location_serialized,
#         'weather': weather_data
#     }
#     logger.debug(f"Response data: {response_data}")
#     return JsonResponse({'status': 'success', 'message': 'Data processed successfully.', 'data': response_data}, status=status.HTTP_200_OK)



# ** Fixing Assertion Error
@api_view(['POST'])
def weather_query(request):
    print("Received request data:", request.data)
    # Ensure only POST requests are handled
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Extract and validate request data
    location_name = request.data.get('location')
    date = request.data.get('date')
    hour = request.data.get('hour')  # Hour can be None

    # Check if location_name is None or empty
    if not location_name:
       return JsonResponse({'status': 'error', 'message': 'Location is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Now we can safely call get_weather_data
        get_weather_data(location_name)
        location = get_location(location_name)
        print("Output from get_location:", location)
        if not location:
            return JsonResponse({'status': 'error', 'message': 'Location does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the location object
        print("Type of location:", type(location))
        print("Content of location:", location)
        location_serialized = LocationSerializer(location).data
        print("Serialized location data:", location_serialized)

        # Now we can safely call get_weather_data
        weather_data = fetch_weather_data(location, date, hour)
        print("Output from fetch_weather_data:", weather_data)
        if not weather_data:
            return JsonResponse({'status': 'error', 'message': 'No weather data available for the specified parameters.'}, status=status.HTTP_404_NOT_FOUND)

    except LocationNotFoundError as e:
        # Handle location not found error
        logger.error(f"LocationNotFoundError caught: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    #except ExternalAPIError as e:
    except RequestException as e:
        # Handle specific known error (e.g., ExternalAPIError is a custom exception)
        logger.error(f"Request error occurred: {e}")
        return JsonResponse({'status': 'error', 'message': 'Failed to retrieve weather data due to an external error.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error occurred: {e}")
        return JsonResponse({'status': e, 'message': 'An unexpected error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Combine location data with weather data
    response_data = {
            'location': location_serialized,
            'weather': weather_data
        }

    print("Final response data:", response_data)
    logger.debug(f"Response data: {response_data}")
    return JsonResponse({'status': 'success', 'message': 'Data processed successfully.', 'data': response_data}, status=status.HTTP_200_OK)





# Clean up
# @api_view(['POST'])
# def weather_query(request):
#     # Ensure only POST requests are handled
#     if request.method != "POST":
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     # Extract and validate request data
#     location_name = request.data.get('location')
#     date = request.data.get('date')
#     hour = request.data.get('hour')  # Hour can be None
#
#     # Check if location_name is None or empty
#     if not location_name:
#        return JsonResponse({'status': 'error', 'message': 'Location is required.'}, status=status.HTTP_400_BAD_REQUEST)
#
#     try:
#         # Check if the location exists in the database
#         location = get_location(location_name)
#         if location:
#             # Location found in database, fetch weather data
#             weather_data = fetch_weather_data(location, date, hour)
#         else:
#             # Location not in database, call get_weather_data to fetch from API
#             weather_data = get_weather_data(location_name)
#
#         # Now we can safely call get_weather_data
#         weather_data = fetch_weather_data(location, date, hour)
#         if not weather_data:
#             return JsonResponse({'status': 'error', 'message': 'No weather data available for the specified parameters.'}, status=status.HTTP_404_NOT_FOUND)
#
#     except LocationNotFoundError as e:
#         # Handle location not found error
#         logger.error(f"LocationNotFoundError caught: {e}")
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
#
#     #except ExternalAPIError as e:
#     except RequestException as e:
#         # Handle specific known error (e.g., ExternalAPIError is a custom exception)
#         logger.error(f"Request error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': 'Failed to retrieve weather data due to an external error.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     except Exception as e:
#         # Handle unexpected errors
#         logger.error(f"Unexpected error occurred: {e}")
#         return JsonResponse({'status': 'error', 'message': 'An unexpected error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     return JsonResponse({'status': 'success', 'message': 'Data processed successfully.', 'data': weather_data}, status=status.HTTP_200_OK)


def get_location(location_name):
    print(location_name)
    location = Location.objects.filter(name=location_name.lower()).first()
    print('L: ', dir(location))
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



# @api_view(['GET', 'POST'])
# def weather_q(request):
#     if request.method == 'GET':
#         locations = Location.objects.all() #.values_list('name', flat=True)
#         print(len(locations))
#         serializer = LocationSerializer(locations, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
#     if request.method == 'POST':
#         location_name = request.data.get('location')
#         date = request.data.get('date')
#         hour = request.data.get('hour')  # Hour can be None
#
#         temp = get_weather_data(location_name)
#
#         print(temp)
#         # Check if location_name is None or empty
#         # if not location_name:
#         #    return JsonResponse({'status': 'error', 'message': 'Location is required.'})
#
#         location = get_location(location_name)
#         if not location:
#             return JsonResponse({'status': 'error', 'message': 'Location does not exist.'})
#
#         # Check if the weather data for the location is in the database
#         existing_data = WeatherData.objects.filter(location=location)
#
#         if not existing_data.exists():
#             weather_data = fetch_save_new_weather_data(location)
#         else:
#             weather_data = get_weather_data(location)
#
#         weather_data = fetch_weather_data(location, date, hour)
#         if not weather_data:
#             return JsonResponse(
#                 {'status': 'error', 'message': 'No weather data available for the specified parameters.'})
#
#         return JsonResponse({'status': 'success', 'message': 'Data processed successfully.', 'data': weather_data})
#
#         #return Response(status=status.HTTP_201_OK)
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})