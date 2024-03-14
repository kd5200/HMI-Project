from rest_framework import serializers
from .models import weather, city

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = weather, city
        fields = ['condition','city','cities,states']  # or specify specific fields