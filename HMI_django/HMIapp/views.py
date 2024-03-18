from django.shortcuts import render
from rest_framework.views import APIView
from .models import weather, city
from .serializer import *
from rest_framework.response import Response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.http import JsonResponse, HttpResponse
import requests
import os
from dotenv import load_dotenv
from .utils import get_weather_info
import numpy as np
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache





class ReactView(APIView):
    def get(self, request):
        output = [{"condition": output.condition,
                   "city": output.city}
                   for output in weather.objects.all()]
        return Response(output)
    
    def post(self, request):
        serializer = serializers.ModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        

def get_cities_from_google_sheet(request):
    # Define the scope and credentials
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/kd/HMI_project/work_project/HMI_django/HMIapp/hmi-cities-data-81fec71b076e.json', scope)

    # Authorize the client
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1Vv7jdrjxzTlAfgLTGYoe_lbLdQB7WgfTNw3Lo5cPn2A/edit#gid=0')
    worksheet = sheet.get_worksheet(0)  # Assuming data is in the first worksheet

    # Fetch the data
    cities = worksheet.col_values(1)  # Assuming cities are in the first column

    # Remove the header if present
    if cities[0] == 'City':
        cities = cities[1:]
    

    # Return the cities as JSON response
    return JsonResponse({'cities': cities})


def get_google_sheets_data(request):
    # Load credentials from the JSON file
    credentials_file = '/Users/kd/HMI_project/work_project/HMI_django/HMIapp/hmi-cities-data-81fec71b076e.json'
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    # Authorize the client
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1Vv7jdrjxzTlAfgLTGYoe_lbLdQB7WgfTNw3Lo5cPn2A/edit#gid=0')
    worksheet = sheet.get_worksheet(0)  # Assuming data is in the first worksheet

    # Fetch the data
    data = worksheet.get_all_records()

    # Extract column headers
    headers = data[0].keys()

    # Convert data into list of dictionaries
    data_list = []
    for row in data:
        data_dict = {}
        for header in headers:
            data_dict[header] = row[header]
        data_list.append(data_dict)

    return JsonResponse(data_list, safe=False)



def get_weather_info(request, cityName):
    load_dotenv()

    api_key = os.getenv('API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
      return {'error': 'Failed to fetch weather information. Please try again later.'}

    



def get_cities_states_by_weather(request):
    # Get the weather condition from the request query parameters
    weather_condition = request.GET.get('weather_condition')

    if not weather_condition:
        return JsonResponse({'message': 'Weather condition parameter is missing'}, status=400)
    


    # List of desired weather conditions
    desired_conditions = ['Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'Atmosphere', 'Clear', 'Clouds']

    weather_condition_lower = weather_condition.lower()


    # Check if the provided weather condition is valid
    if weather_condition_lower not in [condition.lower() for condition in desired_conditions]:
        return JsonResponse({'message': 'Invalid weather condition'}, status=400)

    # Assuming get_google_sheets_data and get_weather_info are defined somewhere
    response = get_google_sheets_data(request)
    all_cities_states = json.loads(response.content.decode('utf-8'))

    weather_api_data = []
    matching_data = []

    # Iterate over each city-state pair
    for city_state in all_cities_states:
        city = city_state['City']
        state = city_state['State']

        
        # Get weather info for each city
        cache_key = f'weather_info_{city}'
        weather_info = cache.get(cache_key)

        if weather_info is None:
    # If weather data is not cached, make a request to the weather API
            weather_info = get_weather_info(request=request, cityName=city)
    # Cache the weather data for future use with a timeout of 1 hour
            cache.set(cache_key, weather_info, timeout=3600)

        # Check if weather_info is in a proper format
        if isinstance(weather_info, dict):
            weather_api_data.append({'City': city, 'Weather': weather_info})

            # Check if the weather for the current city matches the condition
            if "weather" in weather_info and weather_info["weather"][0]["main"] == weather_condition:
                temperature_fahrenheit = round((weather_info['main']['temp'] - 273.15) * 9/5 + 32)
                # Add city, state, temperature in Fahrenheit, and wind speed to matching data
                matching_data.append({
                    'City': city,
                    'State': state,
                    'Temperature_Fahrenheit': temperature_fahrenheit,
                    'Wind_Speed': weather_info['wind']['speed']
                })
        else:
            # Handle the case where weather_info is not in a proper format
            print("Weather info is not in a proper format:", weather_info)

    return JsonResponse({
        
        'matching_data': matching_data
    }, encoder=DjangoJSONEncoder)


# Create your views here.


