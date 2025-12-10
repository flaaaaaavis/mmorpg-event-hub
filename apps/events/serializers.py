from typing import Any
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer[Any]):
    class Meta:
        model = Event
        fields = '__all__'
