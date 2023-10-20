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



#Django Front-End Version
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
#         # If the location exists in the database
#         if location:
#             query_results = WeatherData.objects.filter(location=location, date=date_str)
#             # If weather data for the queried date does not exist, fetch new data
#             if not query_results.exists():
#                 get_weather_data(location_name)  # Ensure this function fetches data for the specific date and location
#
#             # Refresh the query results after potentially fetching new data
#             query_results = WeatherData.objects.filter(location=location, date=date_str)
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



#Django Front-End Version Test 2 (Defining "response_data" from JsonResponses)

# @api_view(['GET', 'POST'])
# def weather_query(request):
#     print("weather_query method called")
#
#     # Default response data
#     response_data = {
#         'status': 'error',
#         'message': 'An unexpected error occurred.'
#     }
#
#     form = WeatherQueryForm(request.POST or None, initial={'date': datetime.now().date()})
#     context = {'form': form}
#
#     # Query all location names and pass them to the context
#     locations = Location.objects.all().values_list('name', flat=True)
#     context['locations'] = list(locations)
#
#     if request.method == "POST" and form.is_valid():
#         print("POST data received:", request.POST)
#
#         location_name = form.cleaned_data['location']
#         date = form.cleaned_data['date']
#         date_str = date.strftime('%Y-%m-%d')
#         hour = form.cleaned_data['hour']
#         confirmed = request.POST.get('confirmed') == "true"
#
#         location = None
#         try:
#             location = Location.objects.get(name=location_name.lower())
#         except ObjectDoesNotExist:
#             pass
#
#         if not location and not confirmed:
#             response_data['message'] = 'Location does not exist. Confirm to add new location.'
#             return JsonResponse(response_data)
#
#         if not location or (location and not WeatherData.objects.filter(location=location, date=date_str).exists()):
#             get_weather_data(location_name)
#
#         query_results = WeatherData.objects.filter(location=location, date=date_str)
#
#         if query_results.exists():
#             entry = query_results.last().data
#             day_data = entry.get(str(date), {})
#             weather_times = day_data.get('weather_times', {})
#
#             context['data'] = []
#
#             for h, hour_data in weather_times.items():
#                 if hour and h != hour:
#                     continue
#                 context['data'].append({'date': date_str, 'hour': h, 'temperature': hour_data.get('temp')})
#
#             response_data = {
#                 'status': 'success',
#                 'message': 'Data processed successfully.',
#                 'data': context['data']
#             }
#
#     return JsonResponse(response_data)






#Debugging issue with processing POST data (Ahidjo)
# @api_view(['GET', 'POST'])
# def weather_query(request):
#     #print("weather_query method called", request.data)
#
#     # Default response data
#     response_data = {
#         'status': 'error',
#         'message': 'An unexpected error occurred.'
#     }
#
#     form = WeatherQueryForm(request.POST or None, initial={'date': datetime.now().date()})
#     context = {'form': form}
#
#     # Query all location names and pass them to the context
#     locations = Location.objects.all().values_list('name', flat=True)
#     context['locations'] = list(locations)

    # if request.method == "POST":
    #     print("weather_query method called", request.data)
    #     location_name = request.data['location']
    #     date = request.data['date']
    #     spl = date.split('-')
    #     dt = datetime(int(spl[0]), int(spl[1]), int(spl[2]))
    #     date_str = dt.strftime('%Y-%m-%d')
    #     assert date_str == date
    #     hour = request.data['hour']
    #     confirmed = request.POST.get('confirmed') == "true"
    #     # if form.is_valid():
    #     #     print("POST data received:", request.POST)
    #     #     print("POST data received:", request.POST)
    #     #
    #     #     location_name = form.cleaned_data['location']
    #     #     date = form.cleaned_data['date']
    #     #     date_str = date.strftime('%Y-%m-%d')
    #     #     hour = form.cleaned_data['hour']
    #     #     confirmed = request.POST.get('confirmed') == "true"
    #     # else:
    #     #     print("Form is not valid.")
    #     #     print("Form errors:", form.errors)
    #
    #     location = None
    #     try:
    #         location = Location.objects.get(name=location_name.lower())
    #     except ObjectDoesNotExist:
    #         pass
    #
    #     if not location and not confirmed:
    #         response_data['message'] = 'Location does not exist. Confirm to add new location.'
    #         return JsonResponse(response_data)
    #
    #     if not location or (location and not WeatherData.objects.filter(location=location, date=date_str).exists()):
    #         get_weather_data(location_name)
    #
    #     query_results = WeatherData.objects.filter(location=location, date=date_str)
    #
    #     if query_results.exists():
    #         entry = query_results.last().data
    #         my_data = None
    #         for elt in entry:
    #             if date_str in list(elt.keys())[0]:
    #                 my_data = elt
    #
    #         print(entry)
    #
    #         # Check if entry is a list and get the first element if it is
    #         if isinstance(entry, list) and entry:
    #             entry = entry[0]
    #         else:
    #             response_data['message'] = 'No data available.'
    #             return JsonResponse(response_data)
    #
    #         day_data = entry[0]
    #         datum = list(my_data.keys())[0]
    #         print(datum, date_str)
    #         assert datum == date_str
    #         weather_times = my_data.get('weather_times', {})
    #
    #         context['data'] = []
    #
    #
    #         for h, hour_data in weather_times.items():
    #             if hour and h != hour:
    #                 continue
    #             context['data'].append({'date': datum, 'hour': h, 'temperature': hour_data.get('temp')})
    #
    #         response_data = {
    #             'status': 'success',
    #             'message': 'Data processed successfully.',
    #             'data': context['data']
    #         }
    #
    # return JsonResponse(response_data)


#Version with simplified data extraction and Error Handling
# @api_view(['GET', 'POST'])
# def weather_query(request):
#     response_data = {
#         'status': 'error',
#         'message': 'An unexpected error occurred.'
#     }
#
#     form = WeatherQueryForm(request.POST or None, initial={'date': datetime.now().date()})
#     context = {'form': form}
#
#     locations = Location.objects.all().values_list('name', flat=True)
#     context['locations'] = list(locations)
#
#     if request.method == "POST":
#         location_name = request.data['location']
#         date = request.data['date']
#         date = request.data['date']
#         spl = date.split('-')
#         dt = datetime(int(spl[0]), int(spl[1]), int(spl[2]))
#         date_str = dt.strftime('%Y-%m-%d')
#         assert date_str == date
#         hour = request.data['hour']
#         confirmed = request.POST.get('confirmed') == "true"
#
#         location = None
#         try:
#             location = Location.objects.get(name=location_name.lower())
#         except ObjectDoesNotExist:
#             response_data['message'] = 'Location does not exist.'
#             return JsonResponse(response_data)
#
#         if not location and not confirmed:
#             response_data['message'] = 'Location does not exist. Confirm to add new location.'
#             return JsonResponse(response_data)
#
#         if not location or (location and not WeatherData.objects.filter(location=location, date=date_str).exists()):
#             get_weather_data(location_name)
#
#         query_results = WeatherData.objects.filter(location=location, date=date_str)
#
#         if query_results.exists():
#             entry = query_results.last().data
#
#             # Ensure entry is as expected
#             if not isinstance(entry, list) or not entry:
#                 response_data['message'] = 'No data available.'
#                 return JsonResponse(response_data)
#
#         for h, hour_data in weather_times.items():
#             if hour and h != hour:
#                 continue
#             context['data'].append({'date': datum, 'hour': h, 'temperature': hour_data.get('temp')})
#
#             # More specific error messages
#             if not context['data']:
#                 response_data['message'] = 'No weather data available for the specified hour.'
#             else:
#                 response_data = {
#                     'status': 'success',
#                     'message': 'Data processed successfully.',
#                     'data': context['data']
#                 }
#
#     return JsonResponse(response_data)



#In this version, I’ve reincorporated:

    # Form handling and location listing.
    # Confirmation check for new locations.
    # Fetching new weather data if it doesn’t exist for the specified location and date.
# @api_view(['GET', 'POST'])
# def weather_query(request):
#     response_data = {
#         'status': 'error',
#         'message': 'An unexpected error occurred.'
#     }
#
#     context = {'data': []}  # Initializing context and context['data']
#
#     if request.method == "POST":
#         location_name = request.data['location']
#         date = request.data['date']
#         hour = request.data.get('hour')  # Hour can be None
#
#         location = Location.objects.filter(name=location_name.lower()).first()
#
#         if location:
#             query_results = WeatherData.objects.filter(location=location, date=date)
#
#             if query_results.exists():
#                 entry = query_results.last().data
#                 date_data = next((e for e in entry if date in e), None)
#
#                 if date_data:
#                     weather_times = date_data[date].get('weather_times', {})
#                     context['data'] = []
#
#                     for h, hour_data in weather_times.items():
#                         if hour and h.zfill(2) != hour.zfill(2):  # Ensure hour format matches
#                             continue
#                         context['data'].append({
#                             'date': date,
#                             'hour': h,
#                             'temperature': hour_data.get('temp')
#                         })
#
#                     if context['data']:
#                         response_data = {
#                             'status': 'success',
#                             'message': 'Data processed successfully.',
#                             'data': context['data']
#                         }
#                     else:
#                         response_data['message'] = 'No weather data available for the specified hour.'
#
#     return JsonResponse(response_data)

from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Location, WeatherData


@api_view(['GET', 'POST'])
def weather_query(request):
    response_data = {
        'status': 'error',
        'message': 'An unexpected error occurred.'
    }

    if request.method == "POST":
        location_name = request.data.get('location')
        date = request.data.get('date')
        hour = request.data.get('hour')  # Hour can be None

        location = Location.objects.filter(name=location_name.lower()).first()

        if location:
            query_results = WeatherData.objects.filter(location=location, date=date)

            if query_results.exists():
                entry = query_results.last().data

                # Check if entry is a list and get the first element if it is
                if isinstance(entry, list):
                    entry = entry[0]

                date_data = entry.get(date, {}).get('weather_times', {})

                response_data['data'] = []

                for h, hour_data in date_data.items():
                    if hour and h.zfill(2) != hour.zfill(2):  # Ensure hour format matches
                        continue
                    response_data['data'].append({
                        'date': date,
                        'hour': h.zfill(2),
                        'temperature': hour_data.get('temp')
                    })

                if response_data['data']:
                    response_data['status'] = 'success'
                    response_data['message'] = 'Data processed successfully.'
                else:
                    response_data['message'] = 'No weather data available for the specified hour.'
            else:
                response_data['message'] = 'No weather data available for the specified date and location.'
        else:
            response_data['message'] = 'Location does not exist.'

    return JsonResponse(response_data)


