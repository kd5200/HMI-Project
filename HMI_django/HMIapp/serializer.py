from rest_framework import serializers
from .models import weather

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = weather
        fields = '__all__'  # or specify specific fields