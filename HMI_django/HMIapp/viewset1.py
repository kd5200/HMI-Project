from rest_framework import viewsets
from .models import weather
from .serializer import ModelSerializer

class ModelViewSet(viewsets.ModelViewSet):
    queryset = weather.objects.all()
    serializer_class = ModelSerializer