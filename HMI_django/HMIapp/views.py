from django.shortcuts import render
from rest_framework.views import APIView
from .models import weather
from .serializer import *
from rest_framework.response import Response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.http import JsonResponse
# from django.http import HttpResponse

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




# Create your views here.


