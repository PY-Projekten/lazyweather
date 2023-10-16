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



# def weather_query(request):
#     initial_data = {
#         'date': datetime.now().date(),
#         'hour': None
#     }
#
#     form = WeatherQueryForm(request.POST or None, initial=initial_data)
#     context = {'form': form}
#
#     if request.method == "POST" and form.is_valid():
#         location = form.cleaned_data['location']
#         date = form.cleaned_data['date']
#         date_str = date.strftime('%Y-%m-%d')  # Convert date to string in the desired format
#         hour = form.cleaned_data['hour']
#
#         try:
#             weather_data = get_weather_data(location)
#             if not weather_data:
#                 context['error_message'] = "No weather data available for the selected location and date."
#             else:
#                 # ... (your existing code to process and add weather_data to the context)
#                 query_results = WeatherData.objects.filter(location=location)
#
#                 if query_results.exists():
#                     entry = query_results.last().data
#                     day_data = entry[0].get(str(date), {})
#                     weather_times = day_data.get('weather_times', {})
#
#                     context['data'] = []
#
#                     if hour:  # An hour is selected
#                         hour_data = weather_times.get(hour, {})
#                         context['data'].append({'date': date_str, 'hour': hour, 'temperature': hour_data.get('temp')})
#                     else:  # No hour is selected, display all hours
#                         for h, hour_data in weather_times.items():
#                             context['data'].append({'date': date_str, 'hour': h, 'temperature': hour_data.get('temp')})
#
#         except Exception as e:
#             context['error_message'] = f"An error occurred while fetching weather data: {e}"
#
#     return render(request, 'weather_query_template.html', context)


def weather_query(request):
    initial_data = {
        'date': datetime.now().date(),
        'hour': None
    }

    # Instantiate the form with initial values
    form = WeatherQueryForm(request.POST or None, initial=initial_data)

    context = {'form': form}

    if request.method == "POST" and form.is_valid():
        location = form.cleaned_data['location']
        date = form.cleaned_data['date']
        date_str = date.strftime('%Y-%m-%d')
        hour = form.cleaned_data['hour']
        # Query for the relevant weather data
        print(f"User Input - Location: {location}, Date: {date}, Hour: {hour}", location.name, location.longitude)
        #db_location = Location.objects.filter(name=location.lower()).first()
        query_results = WeatherData.objects.filter(location_id=location.id, date=date_str)
        # Debugging the query
        if query_results.exists():
            print(f"Database Query Results: {query_results}")
        else:
            print("No data found in the database for the given location and date.")
            #get_weather_data(location)

        if not query_results.exists():  # If data doesn't exist in the database

            # Fetch weather data from the API and update the database
            dt = get_weather_data(location.name)

            print(f"Fetching data from API for Location: {location.name}, Date: {date_str}")
            # Re-query the database after updating
            query_results = WeatherData.objects.filter(location=location, date=date_str)
            print("-------------------")
            print(dt)
            print("-----------------------")

        if query_results.exists():
            entry = query_results.last().data
            #print("Entry data:", entry)
            day_data = entry[0].get(str(date), {})
            weather_times = day_data.get('weather_times', {})

            context['data'] = []

            if hour:  # An hour is selected
                hour_data = weather_times.get(hour, {})
                context['data'].append({'date': date_str, 'hour': hour, 'temperature': hour_data.get('temp')})
            else:  # No hour is selected, display all hours
                for h, hour_data in weather_times.items():
                    context['data'].append({'date': date_str, 'hour': h, 'temperature': hour_data.get('temp')})

    if 'data' in context:
        print(f"Data to be rendered: {context['data']}")
    else:
        print("No data to be rendered yet.")

    return render(request, 'weather_query_template.html', context)










