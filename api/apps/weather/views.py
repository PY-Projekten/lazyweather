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



def weather_query(request):
    form = WeatherQueryForm(request.POST or None)
    context = {'form': form}
    if request.method == "POST":
        if form.is_valid():
            print("Form data: %s", form.cleaned_data)  # Logging the cleaned data

            location = form.cleaned_data['location']
            date = form.cleaned_data['date']
            date = date.strftime('%Y-%m-%d')  # Convert date to string in the desired format
            hour = form.cleaned_data['hour']

            # Query for the relevant weather data
            #print(date)
            query_results = WeatherData.objects.filter(location=location)
            #print("Query results count: %d", query_results.count())  # Logging the count of results

            if query_results.exists():
                entry = query_results.last().data

                day_data = None
                for item in entry:
                    if str(date) in item.keys():
                        day_data = item[str(date)]
                #print(day_data)
                # New logic to extract hour_data
                data_for_date = None
                #print('ENTRY: ', len(entry))
                if 'weather_times' in day_data.keys():
                    data_for_date = day_data['weather_times']
                else:
                    data_for_date = day_data

                print('dfd: ', data_for_date)

                #for item in entry:
                #    print(item)

                if hour:
                    context['data'] = [{'date': date, 'hour': hour, 'temperature': data_for_date[hour]['temp']}]
                else:
                    i = 0
                    for i in range(24):
                        h = '0'+i+''[-2:]
                        context['data'] += [{'date': date, 'hour': h, 'temperature': data_for_date[h]['temp']}]
                        i+=1

                    context['data'] = [entry.data]  # This would pass the entire day's data
            else:
                context['data'] = []
    print(context)

    return render(request, 'weather_query_template.html', context)





