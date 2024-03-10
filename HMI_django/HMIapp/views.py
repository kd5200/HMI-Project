from django.shortcuts import render
from rest_framework.views import APIView
from .models import weather
from .serializer import *
from rest_framework.response import Response
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

# Create your views here.


