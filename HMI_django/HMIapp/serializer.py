from rest_framework import serializers
from .models import weather

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = weather
        fields = ['condition','city']  # or specify specific fields